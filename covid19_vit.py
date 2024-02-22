# -*- coding: utf-8 -*-
"""Covid19-ViT

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JRQ8IuPbjWKdUa7mt3b7GJUqunLzonwU
"""

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'siim-covid19-detection:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-competitions-data%2Fkaggle-v2%2F26680%2F2283525%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240222%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240222T075516Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D3e51039deb17ed0fc09392f077e2d71715cff93dbd47dcc8abbac516746e70f2d65b564b985b70a87224caf053d5d206c2f42a203de891b3579ac0790a5e1f6c28292418f9bbf68450cb411937f40042c987271779231be89f2cf3e49632a7d90b75ab50c3fe276db9ec5d433b8173c7b3621b0ce4ae3ef1ac552f5a7adc867ac5039cde0085db7120714284b3ed73c070e3413a80f3cab3a5af4b312e9112b755223fb8a3a1a0e5eaf78bf4e1951a1ef89c9a2d83dad1d4a9d22ed74760429654f396fbb4aef66ed3a872b33be5f23cf207a8b28ede9d5092b34a68bddadaef94709926302d3425fbdfccb7d28c1e7a86218012529935363379e748cb7312ca,kermany2018:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F17839%2F23942%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240222%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240222T075516Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D521863a8293b256e640b2423be9f9f663280dc725490e07ea4f68cea889a3676700fb26cf6f1a32437b1f327227cced87aa6311e10ee7cdedefed969c6fa361090f557e2b9951d554b5bab932a4619d1f4d07b0b20913ee04307cbde665359c06f926a8f79dc67ec30bfe3ce0805a0b6fec431312bacc6aed8def591ce8dc95ae06c3fd528d89303a85a7cf51e83ef50b28b4e0bd41dc9cf460ff5ce943785559644a4120e6d5add513d4b5849fa0352576fc5ae0726def62a714fa74cb1c684b7f9c6d93a433c3b649d7639da891074c93e7498a04fa73d805105772ea18b3572aee1e02bf3549231b2485b38f0232321de6ac2230a3e1f0f83c973dc98aa8f,siimcovid19-512-jpg-image-dataset:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1351789%2F2283573%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240222%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240222T075516Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D59cc4296f4d92028a3c606b54266c56df5fd62c35d01f8e5304d4e49e387ccf947e79b4733539d44baa8fe7b428e06dd64e2d9605045ea80dc372b81489485b19aaf585efab26ebde34d51a765d3dd148cb42ac71a14b599d07d764feef69009f43f9963801c4a712c28e4215440f27f63b249650dad8394b12cdbc7accb2de715b1e2251059e0c38778cbd712fa23e19b78614729807fdf0c9b0558007baee22936b1f7ac3f2cf7b46a1f1fe9bd32633942b24654232f272975fda547f7aaf5515e3940191fdd90d62c1172a88e420dd5b39155b4a64c8ff7e9743026ef85fa4dcbbb2a75a79bf565730dc4e3ebb5b2c5b5ade1f3470a66bbc5cc2d54331943,siimcovid19-1024-jpg-image-dataset:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F1351786%2F2283993%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240222%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240222T075516Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D856ebdc5154768209a58ed3e73264115ae15cef1206002d9d6a1e86cff135b29d9082da794429967b24bbeadf0330fed6a48f4c1c95039011e2993fad5723b4c5618cdb62e1e101f83e85208061cc88c9c32b6086010004f20b9a06ef75650bbba2ea72bab397b35fe9b35e1f5bc53d8aa1dc2f2976f6b109d788359fdc2b48aa47cfa31618245aa3f0a9700db3051d7c55ac896500732f169dee3a253f17d0a7a1a6c2960210eac1a5544e00fa8f7caaf7cbe48a4dedc65ce6b46d53c141e99cc23561d002d94c870826f7a7f3a1e06ce98706645cc6008ad9c363ce8223471166e5a6a499db45279b3f4fd0dfc1c9da9bcd36e63ea02c72e11ea69585a9254'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

import numpy as np
import pandas as pd
import os
import gc
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa

# Display
from IPython.display import Image, display
import matplotlib.pyplot as plt
import matplotlib.cm as cm


AUTOTUNE = tf.data.experimental.AUTOTUNE

BASE_PATH = '../input/siim-covid19-detection/'
train_study = pd.read_csv(BASE_PATH + 'train_study_level.csv')
train_study.head()

train_image = pd.read_csv(BASE_PATH + 'train_image_level.csv')
train_image.head()

train_study['id'] = train_study['id'].str.replace('_study',"")
train_study.rename({'id': 'StudyInstanceUID'},axis=1, inplace=True)
train_study.head(3)
# df_std.sort_values(by=['StudyInstanceUID'],inplace=True)
train_study.head()

img_size = 512
BASE_PATH = "../input/siimcovid19-{size}-jpg-image-dataset".format(size=img_size)
collection = pd.read_csv(os.path.join(BASE_PATH,"train.csv" ))
collection['filepath'] = [os.path.join(BASE_PATH,"train",id_+'.jpg')for id_ in collection['image_id']]
collection.head()

target = np.array(collection[['Negative for Pneumonia','Typical Appearance','Indeterminate Appearance','Atypical Appearance']])

X_train, X_test, y_train, y_test  = train_test_split(collection.filepath, target, test_size=0.33, random_state=42)
print(f"train shape: {X_train.shape}- y_train shape: {y_train.shape}")
print(f"test shape: {X_test.shape}- y_test shape: {y_test.shape}")

num_classes = 4
input_shape = (512, 512, 1)

learning_rate = 1e-4 #0.001
weight_decay = 0.0001
batch_size = 256
num_epochs = 100
# We'll resize input images to this size
image_size =  256
# Size of the patches to be extract from the input images
patch_size = 20
num_patches = (image_size // patch_size) ** 2
projection_dim = 128 #64
num_heads = 6 #4
# Size of the transformer layers
transformer_units = [
    projection_dim * 2,
    projection_dim,
]
transformer_layers = 3 #8
# Size of the dense layers of the final classifier
mlp_head_units = [256] #[1024, 512]

@tf.function
def load(image_file, target):
    image = tf.io.read_file(image_file)
    image = tf.image.decode_jpeg(image)

    image_ = tf.cast(image, tf.float32)
    return image_, target

train_loader = (
    tf.data.Dataset
    .from_tensor_slices((X_train,y_train))
    .map(load, num_parallel_calls=AUTOTUNE)
    .shuffle(7)
    .batch(batch_size)
)
test_loader = (
    tf.data.Dataset
    .from_tensor_slices((X_test,y_test))
    .map(load, num_parallel_calls=AUTOTUNE)
    .shuffle(7)
    .batch(batch_size)
)

train_batch = (
    tf.data.Dataset
    .from_tensor_slices((X_train,y_train))
    .map(load, num_parallel_calls=AUTOTUNE)
    .shuffle(7)
    .batch(X_train.shape[0]-100)
)
#next(iter(train_batch))[0].shape

data_augmentation = keras.Sequential(
    [
        layers.experimental.preprocessing.Normalization(),
        layers.experimental.preprocessing.Resizing(image_size, image_size),
        layers.experimental.preprocessing.RandomFlip("horizontal"),
        layers.experimental.preprocessing.RandomRotation(factor=0.02),
        layers.experimental.preprocessing.RandomZoom(
            height_factor = 0.2, width_factor = 0.2
        ),
    ],
     name="data_augmentation",
)
# Compute the mean and the variance of the training data for normalization.
CompleteBatchData  =next(iter(train_batch))[0]
data_augmentation.layers[0].adapt(CompleteBatchData)

del CompleteBatchData
gc.collect()

def mlp(x, hidden_units, dropout_rate):
    for units in hidden_units:
        x = layers.Dense(units, activation = tf.nn.gelu)(x)
        x = layers.Dropout(dropout_rate)(x)
    return x

class Patches(layers.Layer):
    def __init__(self, patch_size):
        super(Patches, self).__init__()
        self.patch_size = patch_size

    def call(self, images):
        batch_size = tf.shape(images)[0]
        patches = tf.image.extract_patches(
            images = images,
            sizes = [1, self.patch_size, self.patch_size, 1],
            strides=[1, self.patch_size, self.patch_size, 1],
            rates=[1, 1, 1, 1],
            padding="VALID",
        )
        patch_dims = patches.shape[-1]
        #print(patches.shape)
        patches = tf.reshape(patches, [batch_size, -1, patch_dims])
        return patches

plt.figure(figsize=(8, 8))
image = next(iter(train_loader))[0][5]
plt.imshow(image, cmap='gray')
plt.axis("off")

resized_image = tf.image.resize(
    tf.convert_to_tensor([image]), size=(image_size, image_size)
)
#print(resized_image.shape)
patches = Patches(patch_size)(resized_image)
print(f"Image size: {image_size} X {image_size}")
print(f"Patch size: {patch_size} X {patch_size}")
print(f"Patches per image: {patches.shape[1]}")
print(f"Elements per patch: {patches.shape[-1]}")

n = int(np.sqrt(patches.shape[1]))

plt.figure(figsize=(4, 4))
for i, patch in enumerate(patches[0]):
    ax = plt.subplot(n, n, i + 1)
    patch_img = tf.reshape(patch, (patch_size, patch_size, 1))
    plt.imshow(patch_img,cmap='gray')
    plt.axis("off")

class PatchEncoder(layers.Layer):
    def __init__(self, num_of_patches, projection_dim):
        super(PatchEncoder, self).__init__()
        self.num_patches = num_patches
        self.projection = layers.Dense(units = projection_dim)
        self.position_embedding = layers.Embedding(
            input_dim = num_patches, output_dim = projection_dim
        )

    def call(self, patch):
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        encode = self.projection(patch) + self.position_embedding(positions)
        return encode

def vit_model():
    inputs = layers.Input(shape=input_shape)
    # Augment data.
    augmented = data_augmentation(inputs)
    # Create patches.
    patches = Patches(patch_size)(augmented)
    # Encode patches.
    encoded_patches = PatchEncoder(num_patches, projection_dim)(patches)

    # Create multiple layers of the Transformer block.
    for _ in range(transformer_layers):
        # Layer normalization 1.
        x1 = layers.BatchNormalization()(encoded_patches)
        # create a multi-head attention layer
        attention_output = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=projection_dim, dropout=0.1
        )(x1, x1)
        # Skip connection 1.
        x2 = layers.Add()([attention_output, encoded_patches])
        # Layer normalization 2.
        x3 = layers.BatchNormalization()(x2)
        # MLP.
        x3 = mlp(x3, hidden_units=transformer_units, dropout_rate=0.1)
        # Skip connection 2.
        encoded_patches = layers.Add()([x3, x2])

    # Create a [batch_size, projection_dim] tensor.
    representation = layers.LayerNormalization()(encoded_patches)
    representation = layers.Flatten()(representation)
    representation = layers.Dropout(0.5)(representation)
    # Add MLP
    features = mlp(representation, hidden_units = mlp_head_units, dropout_rate=0.5)
    # Classify outputs.
    logits = layers.Dense(num_classes, activation='softmax')(features)
    # create keras model
    model = keras.Model(inputs=inputs, outputs=logits)
    return model

def experiment(model):
    optimizer = tfa.optimizers.AdamW(
        learning_rate=learning_rate, weight_decay=weight_decay
    )

    model.compile(
        optimizer=optimizer,
        loss=keras.losses.CategoricalCrossentropy(from_logits=True),
        metrics=[
            keras.metrics.CategoricalAccuracy(name="accuracy"),
            keras.metrics.AUC( name="AUC"),
        ],
     )
    checkpoint_filepath = "./tmp/checkpoint"
    checkpoint_callback = keras.callbacks.ModelCheckpoint(
        checkpoint_filepath,
        monitor="val_accuracy",
        save_best_only=True,
        save_weights_only=True,
    )

    history = model.fit(train_loader ,
                        batch_size=batch_size,
                        epochs=num_epochs,
                        validation_data=test_loader,
                        callbacks=[checkpoint_callback],)
    model.load_weights(checkpoint_filepath)
    _, accuracy, auc = model.evaluate(test_loader)
    print(f"Test accuracy: {round(accuracy * 100, 2)}%")
    print(f"Test AUC: {round(auc * 100, 2)}%")

    return history

vit_classifier = vit_model()
vit_classifier.summary()

history = experiment(vit_classifier)

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.figure(figsize=(12,10))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.figure(figsize=(12,10))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.figure(figsize=(12,10))
plt.plot(history.history['AUC'])
plt.plot(history.history['val_AUC'])
plt.title('model AUC')
plt.ylabel('AUC')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

vit_classifier.load_weights("./tmp/checkpoint")

def get_img_array(img):

    # `array` is a float32 Numpy array of shape (299, 299, 3)
    array = keras.preprocessing.image.img_to_array(img)
    # We add a dimension to transform our array into a "batch"
    # of size (1, 299, 299, 3)
    array = np.expand_dims(array, axis=0)
    return array

def gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    # First, we create a model that maps the input image to the activations
    # of the last conv layer as well as the output predictions
    grad_model = tf.keras.models.Model(
        [model.input], [model.get_layer(last_conv_layer_name).output,  model.output]
    )

    # Then, we compute the gradient of the top predicted class for our input image
    # with respect to the activations of the last conv layer
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]


    # This is the gradient of the output neuron (top predicted or chosen)
    # with regard to the output feature map of the last conv layer
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # This is a vector where each entry is the mean intensity of the gradient
    # over a specific feature map channel
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1))
    # We multiply each channel in the feature map array
    # by "how important this channel is" with regard to the top predicted class
    # then sum all the channels to obtain the heatmap class activation
    last_conv_layer_output = last_conv_layer_output#[0]
    #print(np.expand_dims(last_conv_layer_output,axis=0))
    #print(pooled_grads[..., tf.newaxis])
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # For visualization purpose, we will also normalize the heatmap between 0 & 1
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def display_gradcam(img, heatmap, cam_path="cam.jpg", alpha=0.4,preds=[0,0,0,0], plot=None):

    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cm.get_cmap("jet")

    # Use RGB values of the colormap
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # Create an image with RGB colorized heatmap
    jet_heatmap = keras.preprocessing.image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
    jet_heatmap = keras.preprocessing.image.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
    superimposed_img = jet_heatmap * alpha + img
    superimposed_img = keras.preprocessing.image.array_to_img(superimposed_img)

    # Save the superimposed image
    #superimposed_img.save(cam_path)

    # Display Grad CAM
    #display(Image(cam_path))
    #plt.figure(figsize=(8,8))
    plot.imshow(superimposed_img)
    plot.set(title =
        "Negative for Pneumonia: \
        {:.3f}\nTypical Appearance: \
        {:.3f}\nIndeterminate Appearance: \
        {:.3f}\nAtypical Appearance: \
        {:.3f}".format(preds[0], \
                    preds[1], \
                    preds[2], \
                    preds[3])
    )
    plot.axis('off')
    #plt.show()

test_image = next(iter(test_loader))[0][5]
# Prepare image
img_array =get_img_array(test_image)

last_conv_layer_name = 'layer_normalization'
# Remove last layer's softmax
vit_classifier.layers[-1].activation = None
# Print what the top predicted class is
preds = vit_classifier.predict(img_array)
print("Predicted:\n" +"Negative for Pneumonia: \
    {p1}\nTypical Appearance: {p2}\nIndeterminate Appearance: \
    {p3}\nAtypical Appearance: {p4}".format(p1=preds[0][0], \
                                            p2=preds[0][1],p3=preds[0][2],p4=preds[0][3]))
# Generate class activation heatmap
heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

heatmap = np.reshape(heatmap, (12,12))
# Display heatmap
plt.matshow(heatmap)

plt.show()

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][:6], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][20:27], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][50:57], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][60:67], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][70:77], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][100:107], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][200:207], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][250:257], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][150:157], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)

fig, axis = plt.subplots(3, 2, figsize=(20, 20))
for images, ax in zip(next(iter(test_loader))[0][170:177], axis.flat):
    img_array =get_img_array(images)
    # Remove last layer's softmax
    vit_classifier.layers[-1].activation = None
    # Print what the top predicted class is
    preds = vit_classifier.predict(img_array)
    heatmap = gradcam_heatmap(img_array, vit_classifier, last_conv_layer_name)

    heatmap = np.reshape(heatmap, (12,12))
    display_gradcam(images, heatmap, preds=preds[0], plot=ax)
