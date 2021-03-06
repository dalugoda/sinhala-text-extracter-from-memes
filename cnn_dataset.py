import cv2
import os
import glob
from sklearn.utils import shuffle
import numpy as np


def prepare_train_data_set():
    img = cv2.imread("traning_set.jpg")
    # Convert this Image in gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Now we split the image to 5000 cells, each 20x20 size
    cells = [np.array_split(row, 100, 0) for row in np.array_split(gray, 247, 1)]
    # Make it into a Numpy array. It size will be (50,100,20,20)
    rows = np.array(cells)

    base_path = 'cnn_dataset/'

    letter_count = 0
    for row in rows:
        letter_count += 1
        type_count = 0

        character_path = base_path + str(letter_count)
        if not os.path.exists(character_path):
            os.makedirs(character_path)

        print("Creating class : ", letter_count)

        for item in row:
            type_count += 1
            ret, binarized = cv2.threshold(item, 175, 255, 0)
            cv2.imwrite(character_path + '/' + str(letter_count) + '_' + str(type_count) + '.jpg', binarized)
            # cv2.imshow('x', item)
            # cv2.waitKey(0)


def load_train(train_path, image_size, classes):
    images = []
    labels = []
    img_names = []
    cls = []

    print('Going to read training images')
    for fields in classes:
        index = classes.index(fields)
        print('Now going to read {} files (Index: {})'.format(fields, index))
        path = os.path.join(train_path, fields, '*g')
        files = glob.glob(path)
        for fl in files:
            image = cv2.imread(fl, 0)
            image = cv2.resize(image, (image_size, image_size), 0, 0, cv2.INTER_LINEAR)
            image = image.astype(np.float32)
            image = np.multiply(image, 1.0 / 255.0)
            image1 = image.reshape(50, 50, 1)
            images.append(image1)
            label = np.zeros(len(classes))
            label[index] = 1.0
            labels.append(label)
            flbase = os.path.basename(fl)
            img_names.append(flbase)
            cls.append(fields)
    images = np.array(images)
    labels = np.array(labels)
    img_names = np.array(img_names)
    cls = np.array(cls)

    return images, labels, img_names, cls


class DataSet(object):

    def __init__(self, images, labels, img_names, cls):
        self._num_examples = images.shape[0]

        self._images = images
        self._labels = labels
        self._img_names = img_names
        self._cls = cls
        self._epochs_done = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def img_names(self):
        return self._img_names

    @property
    def cls(self):
        return self._cls

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_done(self):
        return self._epochs_done

    def next_batch(self, batch_size):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        self._index_in_epoch += batch_size

        if self._index_in_epoch > self._num_examples:
            # After each epoch we update this
            self._epochs_done += 1
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch

        return self._images[start:end], self._labels[start:end], self._img_names[start:end], self._cls[start:end]


def read_train_sets(train_path, image_size, classes, validation_size):
    class DataSets(object):
        pass

    data_sets = DataSets()

    images, labels, img_names, cls = load_train(train_path, image_size, classes)
    images, labels, img_names, cls = shuffle(images, labels, img_names, cls)

    if isinstance(validation_size, float):
        validation_size = int(validation_size * images.shape[0])

    validation_images = images[:validation_size]
    validation_labels = labels[:validation_size]
    validation_img_names = img_names[:validation_size]
    validation_cls = cls[:validation_size]

    train_images = images[validation_size:]
    train_labels = labels[validation_size:]
    train_img_names = img_names[validation_size:]
    train_cls = cls[validation_size:]

    data_sets.train = DataSet(train_images, train_labels, train_img_names, train_cls)
    data_sets.valid = DataSet(validation_images, validation_labels, validation_img_names, validation_cls)

    return data_sets


# prepare_train_data_set()