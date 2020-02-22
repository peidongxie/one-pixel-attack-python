from base64 import b64encode
from os import remove, walk
from time import time

from PIL.Image import fromarray, open as image_open
from numpy import amax, amin, array, load
from tensorflow.keras.models import load_model

cifar10_test_images = load('static/cifar10_test_images.npy')
cifar10_test_labels = load('static/cifar10_test_labels.npy')
cifar10_cnn = load_model('static/cifar10_cnn.h5')


def file_cleaner():
    for root, dirs, files in walk('static'):
        for file in files:
            if not file.startswith('cifar10'):
                if time() > int(file[:10]) + 36000:
                    remove('static/' + file)
    return


def image_creator(file):
    file_cleaner()
    if isinstance(file, int):
        image = cifar10_test_images[file]
        path = 'static/' + str(int(time())) + '-image.png'
        fromarray((image * 255.0).astype('uint8')).save(path)
        return path
    filename = file.filename
    if filename.endswith('.npy'):
        image = load(file)
        shape = image.shape
        if (len(shape) == 3 and shape[-1] == 3) or (len(shape) == 2 and shape[-1] != 3):
            if amin(image) >= 0:
                if amax(image) <= 1:
                    image = (image * 255.0).astype('uint8')
                elif amax(image) <= 255:
                    image = image.astype('uint8')
                else:
                    return
                path = 'static/' + str(int(time())) + '-' + filename[:-3] + 'png'
                fromarray(image).save(path)
                return path
    elif filename.endswith('.png'):
        path = 'static/' + str(int(time())) + '-' + filename
        file.save(path)
        return path


def base64_loader(path):
    try:
        with open(path, 'rb') as file:
            data = b64encode(file.read()).decode()
            return 'data:image/png;base64,' + data
    except FileNotFoundError:
        return


def model_creator(file):
    file_cleaner()
    path = 'static/' + str(int(time())) + '-' + file.filename
    file.save(path)
    return path


def image_loader(path):
    if not path.endswith('.png'):
        return
    try:
        return array(image_open(path)) / 255.0
    except FileNotFoundError:
        return


def model_loader(path):
    if path == 'static/':
        return cifar10_cnn
    try:
        return load_model(path)
    except FileNotFoundError:
        return


def label_loader(index):
    return int(cifar10_test_labels[index])
