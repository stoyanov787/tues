import pathlib
import wikipedia
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

def test(file_path):
    AUTOTUNE = tf.data.AUTOTUNE
    #file_path = 'C:\Users\ilina\AppData\Local\Programs\Python\Python310\Scripts\minigames\planet_guesser\dataset'
    file_path = pathlib.Path(file_path)

    BATCH_SIZE = 8
    IMG_HEIGHT = 180
    IMG_WIDTH = 180

    train_ds = tf.keras.utils.image_dataset_from_directory(
    file_path,
    validation_split=0.2,  # 20% for validation
    subset="training",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE)

    val_ds = tf.keras.utils.image_dataset_from_directory(
    file_path,
    validation_split=0.2,  # 20% for validation
    subset="validation",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE)

    class_names = train_ds.class_names

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    normalization_layer = layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))
    first_image = image_batch[0]

    num_classes = len(class_names)

    model = Sequential([
    layers.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    epochs = 10
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
    )

    data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal",
                        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ]
    )

    model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Dropout(0.2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
])

    model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])

    epochs = 15
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
    )

    epochs = 15
    history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
    )

    directory = os.listdir('C:\Users\ilina\PycharmProjects\hacktues\planet_guesser\Test')
    file_path = f'C:\Users\ilina\PycharmProjects\hacktues\planet_guesser\Test\{directory[0]}'
    file_path = pathlib.Path(file_path)

    img = tf.keras.utils.load_img(
        file_path, target_size=(IMG_HEIGHT, IMG_WIDTH)
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    planet = f"{class_names[np.argmax(score)]}"
    accuracy = f"{round(100 * np.max(score), 2)}"
    text = wikipedia.summary(f'{planet}(planet)', sentences=2)
    os.remove(f'C:\Users\ilina\PycharmProjects\hacktues\planet_guesser\Test\{directory[0]}')
    return planet

test()
