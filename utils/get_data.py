import os
import numpy as np
import tensorflow as tf
import tensorflow_io as tfio

print("\n", tf.__version__, "\n")
print("\n", tfio.__version__, "\n")

train_img_path = "./data/ds1/train/img/cls"
train_mask_path = "./data/ds1/train/bin_mask/cls"

validation_img_path = "./data/ds1/validation/img/cls"
validation_mask_path = "./data/ds1/validation/bin_mask/cls"

def preprocess(img_path, mask_path):
    img = tf.io.read_file(img_path)
    img = tfio.experimental.image.decode_tiff(img)
    img = tf.cast(img, tf.float32)
    print("Tip imagine:", type(img))
    print("Forma imaginii:", tf.shape(img))
    img = img / 255.0

    mask = tf.io.read_file(mask_path)
    mask = tfio.experimental.image.decode_tiff(mask)
    mask = tf.cast(mask > 0, tf.float32)

    return img, mask

def create_dataset(img_paths, mask_paths, batch_size=8, shuffle=True):
    dataset = tf.data.Dataset.from_tensor_slices((img_paths, mask_paths))
    dataset = dataset.map(lambda x, y: preprocess(x, y), num_parallel_calls=tf.data.AUTOTUNE)
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=100)
        
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset

train_imgs = sorted([ 
    os.path.join(train_img_path, file_name) 
    for file_name in os.listdir(train_img_path)
])

train_masks = sorted([
    os.path.join(train_mask_path, file_name) 
    for file_name in os.listdir(train_mask_path)
])

validation_imgs = sorted([
    os.path.join(validation_img_path, file_name)
    for file_name in os.listdir(validation_img_path)
])

validation_masks = sorted([
    os.path.join(validation_mask_path, file_name)
    for file_name in os.listdir(validation_mask_path)
])

train_dataset = create_dataset(train_imgs, train_masks)
validation_dataset = create_dataset(validation_imgs, validation_masks)
