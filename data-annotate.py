import cv2
import os
import sys
import shutil
import time

segmented_dir = 'annotate_test/segmented/16142986_620504001468084_1148795977560562295_n'
data_set_dir = 'annotate_test/cnn_dataset/'

character_list = []
for (dir_path, dir_names, file_names) in os.walk(segmented_dir):
    character_list.extend(file_names)
    break

for char in character_list:
    char_path = segmented_dir + '/' + char
    img = cv2.imread(char_path)
    cv2.imshow(char, img)
    cv2.waitKey(2)

    label = input("Enter Label for " + char + " : ")
    cv2.destroyWindow(char)

    label_path = data_set_dir + str(label)
    if not os.path.exists(label_path):
        os.makedirs(label_path)

    timestamp = str(time.time()).split('.')[0]
    shutil.move(char_path, label_path + '/' + timestamp + char)
