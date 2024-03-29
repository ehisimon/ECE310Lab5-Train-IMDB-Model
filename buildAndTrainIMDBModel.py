# -*- coding: utf-8 -*-
"""buildAndTrainIMDBModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1crZ_GqhdZ0Wnyu9MLSinmrqEKKiZRwQw
"""

import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub
import os
from google.colab import drive

drive.mount('/content/gdrive')

raw_train_set, raw_valid_set= tfds.load(
  name="imdb_reviews",
  split=["train[:90%]", "train[90%:]"],
  as_supervised=True
)
tf.random.set_seed(42)
train_set = raw_train_set.shuffle(5000, seed=42).batch(32).prefetch(1)
valid_set = raw_valid_set.batch(32).prefetch(1)


for review, label in raw_train_set.take(4):
  print(review.numpy().decode("utf-8")[:200], "...")
  print("Label:", label.numpy())

vocab_size = 1000
text_vec_layer = tf.keras.layers.TextVectorization(max_tokens=vocab_size)
text_vec_layer.adapt(train_set.map(lambda reviews, labels: reviews))

embed_size = 128
tf.random.set_seed(42)

os.environ["TFHUB_CACHE_DIR"] = "my_tfhub_cache"
model = tf.keras.Sequential([
  hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder/4",
  trainable=True, dtype=tf.string, input_shape=[]),
  tf.keras.layers.Dense(64, activation="relu"),
  tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(loss="binary_crossentropy", optimizer="nadam",
              metrics=["accuracy"])
history = model.fit(train_set, validation_data=valid_set, epochs=2)
model.save('/content/gdrive/MyDrive/savedModel')

model.save('/content/gdrive/MyDrive/savedModel')