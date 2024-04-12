import os
import argparse
import datetime

import tensorflow as tf
import tensorflow_datasets as tfds 


# Load the Iris dataset
dataset = tfds.load('iris', as_supervised=True, split='train')
dataset = dataset.batch(10)

# Define a simple model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),  # input shape is 4 because Iris features are 4-dimensional
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')  # output shape is 3 for the three Iris species
])

# Compile the model
model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

# Train the model
model.fit(dataset, epochs=10)

# Save the tarined model at gcs_input_uri
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
model_dir = os.environ['AIP_MODEL_DIR']
gcs_input_uri = f"{model_dir}/model-{timestamp}/"

model.save(gcs_input_uri)