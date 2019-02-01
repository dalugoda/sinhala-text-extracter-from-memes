import cv2
import numpy as np
import os


def crop_image_border(image):

    image_original = image
    ret, image = cv2.threshold(image, 127, 255, 0)

    H, W, C = image.shape
    # Mask of non-black pixels (assuming image has a single channel).
    mask = image > 0

    # Coordinates of non-black pixels.
    coords = np.argwhere(mask)

    # Bounding box of non-black pixels.
    x0, y0, _ = coords.min(axis=0)
    x1, y1, _ = coords.max(axis=0) + 1  # slices are exclusive at the top

    top = x0
    right = W - y1
    left = y0
    bottom = H - x1

    cropped = image_original[x0:x1, y0:y1]
    cropped = cv2.copyMakeBorder(cropped, top=top, bottom=bottom, left=left, right=right, borderType=cv2.BORDER_CONSTANT,
                               value=[255, 255, 255])

    return cropped


def pre_process(base_path, test_path, image_name):

    print("Pre-processing Started...")
    image = cv2.imread(base_path + test_path + image_name)
    height, width, channels = image.shape

    # background
    # create a blank white image
    background_image = np.zeros((height, width, 3), np.uint8)
    # Fill image with red color(set each pixel to white)
    background_image[:] = (255, 255, 255)
    
    # if image size is larger, down sample
    if height > 1100 or width > 1100:
        image = cv2.pyrDown(image)
        background_image = cv2.pyrDown(background_image)

    image = crop_image_border(image)

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(base_path + 'step_1_gray/', image_name), image_gray)
    
    # output threshold image
    ret2, image_output = cv2.threshold(image_gray, 100, 255, 0)
    
    # apply top hat function
    kernel = np.ones((25, 25), np.uint8)
    image_top_hat = cv2.morphologyEx(image_gray, cv2.MORPH_TOPHAT, kernel)
    # cv2.imshow("image_top_hat", image_top_hat)
    cv2.imwrite(os.path.join(base_path + 'step_2_top_hat/', image_name), image_top_hat)
    
    image_dilation = cv2.dilate(image_top_hat, None, iterations=1)
    # cv2.imshow("dilation", image_dilation)
    # cv2.imwrite(os.path.join(base_path + 'step_3_dilate/', image_name), image_dilation)
    
    # image binarization
    ret, thresh = cv2.threshold(image_dilation, 127, 255, 0)
    # cv2.imshow("threshold", thresh)
    cv2.imwrite(os.path.join(base_path + 'step_4_binarize/', image_name), thresh)
    
    morph_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, morph_kernel)
    cv2.imwrite(os.path.join(base_path + 'step_6_connected/', image_name), connected)
    
    mask = np.zeros(thresh.shape, np.uint8)
    # find contours
    im2, contours, hierarchy = cv2.findContours(connected, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    # filter contours
    contour_count = 0
    for idx in range(0, len(hierarchy[0])):
    
        rect = x, y, rect_width, rect_height = cv2.boundingRect(contours[idx])
        # fill the contour
        mask = cv2.drawContours(mask, contours, idx, (255, 255, 255), cv2.FILLED)
    
        # ratio of non-zero pixels in the filled region
        r = float(cv2.countNonZero(mask)) / (rect_width * rect_height)
    
        if r > 0.3 and rect_height > 8 and rect_width > 10 and rect_width > rect_height:
    
            # remove nested contours
            if hierarchy[0, idx, 3] == -1:
                contour_count += 1

                # margins
                m1 = 8
                m2 = 8
                m3 = 8
                m4 = 8

                # if margins going beyond image boundaries, reduce
                if y-m1 < 0:
                    m1 = int(m1/2)

                if y + rect_height + m2 > height:
                    m2 = int(m2/2)

                if x - m3 < 0:
                    m3 = int(m3/2)

                if x + rect_width + m4 > width:
                    m4 = int(m4/2)

                # if margins going beyond image boundaries, ignore the margin
                if y-m1 < 0:
                    m1 = 0

                if y + rect_height + m2 > height:
                    m2 = 0

                if x - m3 < 0:
                    m3 = 0

                if x + rect_width + m4 > width:
                    m4 = 0

                # new vertices
                v1 = (x-m3, y + rect_height+m4)
                v2 = (x + rect_width+m4, y-m1)
    
                # draw rectangle
                image = cv2.rectangle(image, v1, v2, (0, 255, 0), 2)
    
                # region of interest
                roi = image_output[y - m1:y + rect_height + m2, x - m3:x + rect_width + m4]
    
                try:
                    roi_co = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
                    background_image[y - m1:y + rect_height + m2, x - m3:x + rect_width + m4] = roi_co

                except cv2.error as e:
                    print('conversion error occurred. skipped...')

    cv2.imwrite(os.path.join(base_path + 'step_5_roi/', image_name), image)
    cv2.imwrite(os.path.join(base_path + 'step_7_output/', image_name), background_image)
    # cv2.imshow('image', image)
    # cv2.imshow('back', background_image)
    # cv2.waitKey(0)

    print("Pre-processing Done")
