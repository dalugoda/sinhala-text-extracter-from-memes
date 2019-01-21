import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def character_segment(base_path, character_segments_path, image_name):
    print(image_name)
    base_image_name_array = image_name.split('.')
    path = base_path + character_segments_path + base_image_name_array[0] + '/'

    line_list = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        line_list.extend(file_names)
        break

    sorted_word_list = []

    for i in range(len(line_list)):
        image_name = line_list[i]
        image_name_array = image_name.split('.')
        new_image_name = image_name_array[0].replace('_', '.')
        sorted_word_list.append(float(new_image_name))

    sorted_word_list.sort()

    character_segment_base_path = 'step_11_character_segment/'
    character_segmented_path = character_segment_base_path + 'segmented/' + base_image_name_array[0]

    if not os.path.exists(base_path + character_segmented_path):
        os.makedirs(base_path + character_segmented_path)

    for i in range(len(sorted_word_list)):

        reset_image_name = str(sorted_word_list[i]).replace('.', '_')

        line_segment_original = cv2.imread(path + reset_image_name + '.' + base_image_name_array[1])
        line_segment = cv2.imread(path + reset_image_name + '.' + base_image_name_array[1], 0)

        line_segment = 255 - line_segment
        line_segment_sum = np.sum(line_segment, axis=0).tolist()

        line_segment_sum[0] = 0
        line_segment_sum[len(line_segment_sum) - 1] = 0

        # ignore counts less than 800
        for x in range(len(line_segment_sum)):
            if line_segment_sum[x] < 800:
                line_segment_sum[x] = 0

        print(line_segment_sum)

        # identify rising points and falling points
        cords = []
        for x in range(len(line_segment_sum) - 1):
            current_value = line_segment_sum[x]
            next_value = line_segment_sum[x + 1]

            if current_value == 0 and next_value == 0:
                continue
            elif current_value > 0 and next_value > 0:
                continue
            elif current_value == 0 and next_value > 0:
                cords.append(x + 1)
            elif current_value > 0 and next_value == 0:
                cords.append(x)

        print(cords)

        H, W = line_segment.shape[:2]

        differences = []

        # get line differences
        for x in range(len(cords) - 1):
            current_value = cords[x]
            next_value = cords[x + 1]

            difference = next_value - current_value

            # filter values
            if 1 < difference < 100:
                differences.append(difference)
            else:
                differences.append(0)

        print(differences)

        # detect pairs
        pairs = []
        for x in range(len(differences)):

            pair = []
            if 1 < differences[x] < 80:
                pair.append(cords[x])
                pair.append(cords[x + 1])
                pairs.append(pair)

        line_segment = 255 - line_segment

        print(pairs)


        character_cords = [0]

        for x in range(len(pairs)):

            pair = pairs[x]

            roi = line_segment[0:H, pair[0]:pair[1]]

            # count black pixels
            black_pixel_count = np.sum(roi == 0)

            # print(pair, " : ", black_pixel_count)

            if black_pixel_count < 15:
                character_cords.append(pair[0])
                character_cords.append(pair[1])

        character_cords.append(W)

        print(character_cords)

        # arrange new pairs
        arranged_pairs = []
        for x in range(0, len(character_cords), 2):
            if character_cords[x] != character_cords[x + 1]:
                pair = [character_cords[x], character_cords[x + 1]]
                arranged_pairs.append(pair)
        print(arranged_pairs)
        # draw new lines
        for x in range(len(arranged_pairs)):
            pair = arranged_pairs[x]
            roi = line_segment[0:H, pair[0]:pair[1]]

            cv2.line(line_segment_original, (pair[0], 0), (pair[0], H), (0, 0, 255), 1)
            cv2.line(line_segment_original, (pair[1], 0), (pair[1], H), (255, 0, 0), 1)

            cv2.imwrite(os.path.join(base_path + character_segmented_path,
                                     str(i) + '_' + str(x) + '.' + base_image_name_array[1]), roi)

        print("----------------------------------")

        # cv2.imwrite(os.path.join(base_path + character_segmented_path + (base_image_name_array[0] + str(i) + '.' + base_image_name_array[1])), line_segment_original)
        # cv2.imshow('segmented', line_segment_original)
        # plt.plot(line_segment_sum)
        # plt.show()
        # cv2.waitKey(0)
