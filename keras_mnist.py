# coding=utf-8
'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''
from __future__ import print_function
import numpy as np

import missinglink

np.random.seed(1337)  # for reproducibility
import argparse
import os

import pwd

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras import backend as K


def get_username():
    return pwd.getpwuid(os.getuid())[0]

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--owner-id', required=True)
parser.add_argument('--project-token', required=True)
parser.add_argument('--epochs', type=int, default=8)
parser.add_argument('--host')

args = parser.parse_args()

batch_size = 128
nb_classes = 10

# input image dimensions
img_rows, img_cols = 28, 28
# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)

# the data, shuffled and split between train and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

if K.image_dim_ordering() == 'th':
    X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
    X_test = X_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
    X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print('X_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

model.add(Convolution2D(
    nb_filters, kernel_size[0], kernel_size[1],
    input_shape=input_shape))

model.add(Activation('relu'))
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))

model.compile(
    loss='categorical_crossentropy',
    optimizer='adadelta',
    metrics=['accuracy'])

callback = missinglink.KerasCallback(owner_id=args.owner_id, project_token=args.project_token, host=args.host)
callback.set_properties(display_name='KerasTEst', description='cool kerassing around')

model.fit(
    X_train, Y_train, batch_size=batch_size, nb_epoch=args.epochs, validation_split=0.2,
    callbacks=[callback])

score = model.evaluate(X_test, Y_test, verbose=0)

print('Test score:', score[0])
print('Test accuracy:', score[1])

FROM missinglinkai/jenkins-k8s-slave:sdk

RUN pip install missinglink-sdk

ADD ./keras_mnist.py

CMD python keras_mnist.py \
    --owner-id 381d23e4-d368-508f-f19b-48c3d8420c60 \
    --project-token YCbtEryxyosBKYgx \
    --epochs 2 \
    --host https://missinglink-staging.appspot.com