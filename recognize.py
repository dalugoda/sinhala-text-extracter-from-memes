import codecs
import os
import unicode_converter
import cnn_predict
import cv2


def get_label_mapper():

    class_file = codecs.open("wijesekara_map.txt", "r", "utf-8")
    classes = class_file.read().split("\t")
    class_file.close()

    return classes


def predict_sentence(base_path, character_segments_path, image_name):
    print("Recognizing Started...")

    base_image_name_array = image_name.split('.')
    path = base_path + character_segments_path + base_image_name_array[0] + '/'

    label_mapper = get_label_mapper()

    character_list = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        character_list.extend(file_names)
        break

    word_list = dict()

    for i in range(len(character_list)):
        image_name = character_list[i].split('.')[0]
        key = int(image_name.split("_")[0])
        value = int(image_name.split("_")[1])

        if key in word_list:
            # append the new number to the existing array at this slot
            word_list[key].append(value)
        else:
            # create a new array in this slot
            word_list[key] = [value]

    predictions = []
    predict_count = len(character_list)
    for word, char_list in sorted(word_list.items()):

        for char in sorted(char_list):
            char_image = cv2.imread(path + str(word) + '_' + str(char) + '.' + base_image_name_array[1], 0)
            first_prob, first_class = cnn_predict.get_prediction(char_image)
            predict_label = label_mapper[int(first_class) - 1]
            # print(predict_label)
            predict_count -= 1
            print("Remaining Characters :", predict_count)
            predictions.append(predict_label)

        predictions.append(' ')

    print("Recognizing Completed. Unicode Mapping Started...")
    sentence_predicted = ''.join(predictions)
    labelled_file_write = codecs.open(base_path + 'step_12_predict/' + base_image_name_array[0] + ".txt", "w", "utf-8")
    labelled_file_write.write(sentence_predicted)
    labelled_file_write.close()

    unicode_mapper = unicode_converter.get_unicode_mapper()
    unicode_sentence = unicode_converter.get_unicode_text(unicode_mapper, sentence_predicted)

    unicode_file_write = codecs.open(base_path + 'step_13_unicode_convert/' + base_image_name_array[0] + ".txt", "w", "utf-8")
    unicode_file_write.write(unicode_sentence)
    unicode_file_write.close()

    print("Unicode Mapping Completed.")

    return unicode_sentence

