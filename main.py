import memes_remove as mr
import pre_process as pp
import segment_line as ls
import segment_word as ws
import segment_character as cs
from os import walk

base_path = 'test/'
test_items_path = 'test_items/'
pre_process_path = 'step_0_faces_remove/'
pre_processed_path = 'step_7_output/'
line_segments_path = 'step_9_vertical_projection_filtered/segmented/'
words_segments_path = 'step_10_word_segment/segmented/'

image_list = []
for (dir_path, dir_names, file_names) in walk(base_path + test_items_path):
    image_list.extend(file_names)
    break


for i in range(len(image_list)):
    mr.remove_meme_faces(base_path, test_items_path, image_list[i])
    pp.pre_process(base_path, pre_process_path, image_list[i])
    ls.line_segment(base_path, test_items_path, pre_processed_path, image_list[i])
    ws.word_segment(base_path, line_segments_path, image_list[i])
    cs.character_segment(base_path, words_segments_path, image_list[i])

