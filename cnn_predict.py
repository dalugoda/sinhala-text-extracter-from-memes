import tensorflow as tf
import numpy as np
import os, glob, cv2
import sys, argparse
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def get_result(image):
    # classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    classes = np.arange(start=1, stop=239).astype(str).tolist()

    letters = {
        "1": '\u0D85',
        "2": '\u0D86',
        "3": '\u0D87',
        "4": '\u0D88',
        "5": '\u0D89',
        "6": '\u0D8A',
        "7": '\u0D8B',
        "8": '\u0D8C',
        "9": '\u0D91',
        "10": '\u0D92',
        "11": '\u0D94',
        "12": '\u0D95',
        "13": '\u0D96'

    }
    # First, pass the path of the image
    image_size = 50
    num_channels = 1
    images = []

    # Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = cv2.resize(image, (image_size, image_size), 0, 0, cv2.INTER_LINEAR)
    # print(len(image[0]))
    print(image.shape)
    # image1 = image.reshape(50, 50, 1)
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0 / 255.0)
    # The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
    x_batch = images.reshape(1, image_size, image_size, num_channels)

    # Let us restore the saved model
    sess = tf.Session()

    # Step-1: Recreate the network graph. At this step only graph is created.
    saver = tf.train.import_meta_graph('cnn_model/character-model.meta')
    # Step-2: Now let's load the weights saved using the restore method.
    saver.restore(sess, tf.train.latest_checkpoint('cnn_model/'))

    # Accessing the default graph which we have restored
    graph = tf.get_default_graph()

    # Now, let's get hold of the op that we can be processed to get the output.
    # In the original network y_pred is the tensor that is the prediction of the network
    y_pred = graph.get_tensor_by_name("y_pred:0")

    # Let's feed the images to the input placeholders
    x = graph.get_tensor_by_name("x:0")
    y_true = graph.get_tensor_by_name("y_true:0")
    y_test_images = np.zeros((238, 238))
    print(y_test_images)

    # Creating the feed_dict that is required to be fed to calculate y_pred
    feed_dict_testing = {x: x_batch, y_true: y_test_images}
    result = sess.run(y_pred, feed_dict=feed_dict_testing)
    # result is of this format [probabiliy_of_rose probability_of_sunflower]
    # print('Maximum probability:', result.max())
    # characters=['ං','අ','ඉ','උ','එ','ඒ']
    first_prob = result.max()
    # print('Maximum probability class:', letters[str(classes[result.argmax()])])
    # first_class = letters[str(classes[result.argmax()])]
    first_class = classes[result.argmax()]
    sortArray = result[0, np.argsort(result)]
    # print('Second Maximum probability:', sortArray[0, -2])
    second_prob = sortArray[0, -2]
    # result[0, result.argmax()] = 0
    # #print('Second Maximum probability class:', letters[str(classes[result.argmax()])])
    # second_class = letters[str(classes[result.argmax()])]
    # tf.reset_default_graph()
    return first_prob, first_class


image = cv2.imread("test/step_11_character_segment/segmented/15326324_602121043306380_4760328155269509500_n/26_0.jpg", 0)
print(get_result(image))
