import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os

# We will fix our image size to (128,128), and image channels will be 3.
img_width = 128
img_height = 128
img_size = (img_width, img_height)
img_channels = 3

Directory = os.listdir("dataset/Train")
Directory.sort()

labels = []
for name in Directory:
    label = name.split('.')[0]
    if label == 'earth':
        labels.append(1)
    else:
        labels.append(0)

df = pd.DataFrame({
    'filename': Directory,
    'label': labels
})

print(df)

model = Sequential()

model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(128, 128, 3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(2, 2))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

print(model.summary())


earlystop = EarlyStopping(patience=10)
learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                            patience=2,
                                            verbose=1,
                                            factor=0.5,
                                            min_lr=0.00001)
callbacks = [earlystop, learning_rate_reduction]

df["label"] = df["label"].replace({0: 'Mars', 1: 'Earth'})
print(df)
train_data, validation_data = train_test_split(df, test_size=0.20, random_state=42)  # train_test_split from sklearn
print(list(train_test_split(df, test_size=0.20, random_state=42)))
train_data = train_data.reset_index(drop=True)
validation_data = validation_data.reset_index(drop=True)

final_train_data = train_data.shape[0]
print(final_train_data)
final_validation_data = validation_data.shape[0]
print(final_validation_data)
batch_size = 1

# ImageDataGenerator from keras.preprocessing.image
generate_train_data = ImageDataGenerator(rotation_range=15,
                                         rescale=1./255,
                                         shear_range=0.1,
                                         zoom_range=0.2,
                                         horizontal_flip=True,
                                         width_shift_range=0.1,
                                         height_shift_range=0.1
                                         )

train_gen = generate_train_data.flow_from_dataframe(train_data,
                                                    "dataset/Train", x_col='filename', y_col='label',
                                                    target_size=img_size,
                                                    class_mode='categorical',
                                                    batch_size=batch_size
                                                    )

generate_validation_data = ImageDataGenerator(rescale=1./255)
validation_gen = generate_validation_data.flow_from_dataframe(
    validation_data,
    "dataset/Train",
    x_col='filename',
    y_col='label',
    target_size=img_size,
    class_mode='categorical',
    batch_size=batch_size
)

epochs = 10
history = model.fit_generator(
    train_gen,
    epochs=epochs,
    validation_data=validation_gen,
    validation_steps=final_validation_data // batch_size,
    steps_per_epoch=final_train_data // batch_size,
    callbacks=callbacks
)


model.save("planets.h5")

test_filenames = os.listdir("dataset/Train")
test_data = pd.DataFrame({
    'filename': test_filenames
})
nb_samples = test_data.shape[0]

generate_test_data = ImageDataGenerator(rescale=1./255)
test_gen = generate_test_data.flow_from_dataframe(
    test_data,
    "dataset/Train",
    x_col='filename',
    y_col=None,
    class_mode=None,
    target_size=img_size,
    batch_size=batch_size,
    shuffle=False
)

prediction = model.predict_generator(test_gen, steps=np.ceil(nb_samples/batch_size))

test_data['label'] = np.argmax(prediction, axis=-1)

label_map = dict((v, k) for k, v in train_gen.class_indices.items())
test_data['label'] = test_data['label'].replace(label_map)

test_data['label'] = test_data['label'].replace({'Earth': 1, 'Mars': 0})

testing = test_data.head(10)
testing.head()
plt.figure(figsize=(12, 24))
for index, row in testing.iterrows():
    filename = row['filename']
    label = row['label']
    image = load_img("dataset/Train/" + filename, target_size=img_size)
    plt.subplot(6, 3, index + 1)
    plt.imshow(image)
    print(label)
    plt.xlabel(filename + '(' + "{}".format(label) + ')')
plt.tight_layout()
plt.show()
