"""
Simple MNIST data parser written in python.
https://github.com/sorki/python-mnist

Author: Richard Marko <rissko@gmail.com>

MNIST is a database of handwritten digits
available on http://yann.lecun.com/exdb/mnist/.

Usage:

        from mnist import MNIST
        mndata = MNIST('./dir_with_mnist_data_files')
        mndata.load_training()
        mndata.load_testing()

Distributed under GNU General Public Licence

"""


import os
import struct
from array import array
from PIL import Image
from PIL import ImageOps
import numpy


class MNIST(object):
    def __init__(self, path='.'):
        self.path = path

        self.test_img_fname = 't10k-images.idx3-ubyte'
        self.test_lbl_fname = 't10k-labels.idx1-ubyte'

        self.train_img_fname = 'train-images.idx3-ubyte'
        self.train_lbl_fname = 'train-labels.idx1-ubyte'

        self.test_images = []
        self.test_labels = []

        self.train_images = []
        self.train_labels = []

    def load_testing(self):
        ims, labels = self.load(os.path.join(self.path, self.test_img_fname),
                                os.path.join(self.path, self.test_lbl_fname))

        self.test_images = ims
        self.test_labels = labels

        return ims, labels

    def load_training(self):
        ims, labels = self.load(os.path.join(self.path, self.train_img_fname),
                                os.path.join(self.path, self.train_lbl_fname))

        self.train_images = ims
        self.train_labels = labels

        return ims, labels

    @classmethod
    def load(cls, path_img, path_lbl):
        with open(path_lbl, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049,'
                                 'got %d' % magic)

            labels = array("B", file.read())

        with open(path_img, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051,'
                                 'got %d' % magic)

            image_data = array("B", file.read())

        images = []
        for i in xrange(size):
            images.append([0] * rows * cols)

        for i in xrange(size):
            images[i][:] = image_data[i * rows * cols: (i + 1) * rows * cols]

        return images, labels

    def test(self):
        test_img, test_label = self.load_testing()
        train_img, train_label = self.load_training()
        assert len(test_img) == len(test_label)
        assert len(test_img) == 10000
        assert len(train_img) == len(train_label)
        assert len(train_img) == 60000
        print 'Showing num:%d' % train_label[0]
        print self.display(train_img[0])
        print
        return True

    @classmethod
    def display(cls, img, width=28):
        render = ''
        for i in range(len(img)):
            if i % width == 0:
                render += '\n'
            if img[i] > 200:
                render += '1'
            else:
                render += '0'
        return render

    def render_image(self, image, path):
        """ Function by Nox
            https://github.com/sorki/python-
            mnist/commit/82c63e7dea77c372786a17087cebd82e0455100f
        """
        l = []
        for y in xrange(28):
            t = []
            for x in xrange(28):
                pixel = image[y * 28 + x]
                t.append([pixel, pixel, pixel])
            l.append(t)
        image = Image.fromarray(numpy.uint8(l))
        image = ImageOps.invert(image)
        image.save(path)

if __name__ == "__main__":
#    print 'Testing'
#    mn = MNIST('.')
#    if mn.test():
#        print 'Passed'

    """ Test by Nox
    """
    dataDir = "../data/mnist"
    mn = MNIST(dataDir)
    images, labels = mn.load_training()
    mn.render_image(images[0], dataDir + "/images/test.png")