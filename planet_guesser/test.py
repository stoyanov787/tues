from main import *
import numpy as np
import os

directory = os.listdir('/home/george/Python/planet_guesser/Test')
file_path = f'/home/george/Python/planet_guesser/Test/{directory[0]}'
file_path = pathlib.Path(file_path)

img = tf.keras.utils.load_img(
    file_path, target_size=(IMG_HEIGHT, IMG_WIDTH)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

with open('result.json', 'w') as file:
    planet = class_names[np.argmax(score)]
    accuracy = round(100 * np.max(score), 2)
    result_dict = {planet: accuracy}
    file.write(f'{result_dict}')

os.remove(f'/home/george/Python/planet_guesser/Test/{directory[0]}')