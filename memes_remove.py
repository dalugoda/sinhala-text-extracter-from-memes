from memes_detector.detector import ObjectDetector
import cv2
import os


def remove_meme_faces(base_path, test_path, image_name):

    detector = ObjectDetector(loadPath="memes_svm.svm")

    image = cv2.imread(base_path + test_path + image_name)
    result = detector.detect(image)

    for (x, y, xb, yb) in result:
        image[y:y+(yb-y), x:x+(xb-x)] = (255, 255, 255)

    cv2.imwrite(os.path.join(base_path + 'step_0_faces_remove/', image_name), image)
    # cv2.imshow("Detected", image)
    # cv2.waitKey(0)
