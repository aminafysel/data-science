# -*- coding: utf-8 -*-
"""Image recognition

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oPYmHswhnMgXTul_7lDiBrblbYGxbWMp
"""

!nvidia-smi

!pip install tensorflow-gpu

import tensorflow as tf
tf.__version__

#importing libraries
from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.models import load_model
from keras.applications.vgg16 import VGG16
from keras.applications.inception_v3 import InceptionV3
from keras.applications.vgg16 import preprocess_input
from keras import layers 
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
import matplotlib.pyplot as plt

#resizing image
IMAGE_SIZE = [224, 224]

#importing datasets
train_path='/content/drive/My Drive/Qburst Internship/Project :Snake Identification/Train'
test_path='/content/drive/My Drive/Qburst Internship/Project :Snake Identification/Test'
valid_path='/content/drive/My Drive/Qburst Internship/Project :Snake Identification/valid'



#Image augmentation

train_datagen = ImageDataGenerator(rescale = 1./255., shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)


test_datagen = ImageDataGenerator( rescale = 1.0/255. )

validation_datagen=ImageDataGenerator(rescale = 1.0/255.)

training_set = train_datagen.flow_from_directory(train_path, batch_size = 32, class_mode = 'binary', target_size = (224, 224))


test_set = test_datagen.flow_from_directory(test_path,  batch_size = 32, class_mode = 'binary', target_size = (224, 224))

#Defining model
base_model = VGG16(input_shape = (224, 224, 3),include_top = False, weights = 'imagenet')
#base_model = InceptionV3(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

#no need to train all layers,making them untrainable
for layer in base_model.layers:
    layer.trainable = False

#Compiling
# Flatten the output layer to 1 dimension
x = layers.Flatten()(base_model.output)

# Add a fully connected layer with 512 hidden units and ReLU activation
#x = layers.Dense(512,activation='relu')(x)

#Add a dropout rate of 0.5
x = layers.Dropout(0.5)(x)

# Add a final layer for classification
x = layers.Dense(1, activation='sigmoid')(x)

model = tf.keras.models.Model(base_model.input, x)

model.compile(optimizer = tf.keras.optimizers.RMSprop(lr=0.00001), loss = 'binary_crossentropy',metrics = ['accuracy'])

model.summary()

# fit the model
vggfit= model.fit_generator(training_set,epochs = 100,steps_per_epoch=5)
#inceptionfit= model.fit_generator(training_set,validation_data = validation_set,epochs=5,steps_per_epoch=len(training_set),validation_steps=len(validation_set))

"""PREDICTION USING TRAINED MODEL"""

#save the model
model.save('snake_recognition_model.h5')

test_image =image.load_img('/content/drive/My Drive/Qburst Internship/Project :Snake Identification/Test/snake/images (31).jpg',target_size =(224,224))
test_image =image.img_to_array(test_image)
test_image =np.expand_dims(test_image, axis =0)
result = model.predict(test_image)
if result[0][0] ==1 :
    prediction = 'There is a presence of snake'
else:
    prediction = 'No presence of snake'
print(prediction)

import matplotlib.image as mpimg
img=mpimg.imread('/content/drive/My Drive/Qburst Internship/Project :Snake Identification/Test/snake/images (31).jpg')
imgplot=plt.imshow(img)
plt.show()

test_image =image.load_img('/content/drive/My Drive/Qburst Internship/Project :Snake Identification/Test/no snake/images - 2020-09-09T130821.671.jpg',target_size =(224,224))
test_image =image.img_to_array(test_image)
test_image =np.expand_dims(test_image, axis =0)
result = model.predict(test_image)
if result[0][0] ==1 :
    prediction = 'There is a presence of snake'
else:
    prediction = 'No presence of snake'
print(prediction)

import matplotlib.image as mpimg
img=mpimg.imread('/content/drive/My Drive/Qburst Internship/Project :Snake Identification/Test/no snake/images - 2020-09-09T130821.671.jpg')
imgplot=plt.imshow(img)
plt.show()