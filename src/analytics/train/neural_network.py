# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import KFold
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import pickle

training_dict = pickle.load(open('output/training_data.pkl', 'rb'))
tlen = int(len(training_dict['labels'])*0.8)
#np.random.shuffle(train_data)
train_images, train_labels, test_images, test_labels = np.array(training_dict['vectors'][:tlen], dtype=float), np.array(training_dict['labels'][:tlen], dtype=float), \
                                                       np.array(training_dict['vectors'][tlen:], dtype=float), np.array(training_dict['labels'][tlen:], dtype=float)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=train_images.shape[1:]),
    keras.layers.Dense(35, activation='sigmoid'),
    keras.layers.Dense(2, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
print("===============================================================")
print(np.array(train_images).shape)
print(np.array(train_labels).shape)
print("===============================================================")
model.fit(np.array(train_images), np.array(train_labels), epochs=1000)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)

print("Saving model...")
model.save('output/predictive_model.model') 

