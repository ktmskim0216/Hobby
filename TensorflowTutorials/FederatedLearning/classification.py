# https://www.tensorflow.org/federated/tutorials/federated_learning_for_image_classification

from __future__ import absolute_import, division, print_function

import collections
import warnings
from six.moves import range
import numpy as np
import six
import tensorflow as tf
import input_data

warnings.simplefilter('ignore')

tf.compat.v1.enable_v2_behavior()

import tensorflow_federated as tff

np.random.seed(0)

NUM_CLIENTS = 10

# NOTE: If the statement below fails, it means that you are
# using an older version of TFF without the high-performance
# executor stack. Call `tff.framework.set_default_executor()`
# instead to use the default reference runtime.
if six.PY3:
  tff.framework.set_default_executor(
      tff.framework.create_local_executor(NUM_CLIENTS))

print('If tff was installed successfully, then it print out "Hello, World!"')
print(tff.federated_computation(lambda: 'Hello, World!')())

## Define preprocessing function
NUM_CLIENTS = 10
NUM_EPOCHS = 10
BATCH_SIZE = 20
SHUFFLE_BUFFER = 500

def preprocess(dataset):

  def element_fn(element):
    return collections.OrderedDict([
        ('x', tf.reshape(element['pixels'], [-1])),
        ('y', tf.reshape(element['label'], [1])),
    ])

  return dataset.repeat(NUM_EPOCHS).map(element_fn).shuffle(
      SHUFFLE_BUFFER).batch(BATCH_SIZE)

## data
mnist = input_data.read_data_sets('/home/harny/Github/DeepTraffic/2.encrypted_traffic_classification/3.PerprocessResults/12class/SessionAllLayers')
example_dataset = tf.data.Dataset.from_tensor_slices({'pixels': mnist.train.images, 'label': mnist.train.labels})
print(example_dataset)

ti = np.array_split(mnist.train.images, NUM_CLIENTS)
tl = np.array_split(mnist.train.labels, NUM_CLIENTS)
data_set = list()
for i in range(len(ti)):
    data_set.append((ti[i], tl[i]))

preprocessed_example_dataset = preprocess(example_dataset)
print(preprocessed_example_dataset)

sample_batch = tf.nest.map_structure(
    lambda x: x.numpy(), iter(preprocessed_example_dataset).next())

print('Check the sample batch dataset: ')
print(sample_batch)

## Make subset for federated data
def make_federated_data(dataset):
  result = list()
  for ti, tl in dataset:
    dd = tf.data.Dataset.from_tensor_slices({'pixels': ti, 'label': tl})
    result.append(preprocess(dd))
  return result

federated_train_data = make_federated_data(data_set)



## create federated model
def create_compiled_keras_model():
  model = tf.keras.models.Sequential([
      tf.keras.layers.Dense(
          12, activation=tf.nn.softmax, kernel_initializer='zeros', input_shape=(784,))])

  model.compile(
      loss=tf.keras.losses.SparseCategoricalCrossentropy(),
      optimizer=tf.keras.optimizers.SGD(learning_rate=0.02),
      metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])
  return model


## create model function
def model_fn():
  keras_model = create_compiled_keras_model()
  return tff.learning.from_compiled_keras_model(keras_model, sample_batch)

iterative_process = tff.learning.build_federated_averaging_process(model_fn)

print('The federated process: ')
print(str(iterative_process.initialize.type_signature))

state = iterative_process.initialize()

state, metrics = iterative_process.next(state, federated_train_data)
print('round  1, metrics={}'.format(metrics))
for round_num in range(2, 11):
  state, metrics = iterative_process.next(state, federated_train_data)
  print('round {:2d}, metrics={}'.format(round_num, metrics))
