# -*- coding: utf-8 -*-
"""cnn-for-diabetic-retinopathy-classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vhtKzz6C800fzQlSwngXPIhcvWL8QdDb
"""

import os
iskaggle = os.environ.get('KAGGLE_KERNEL_RUN_TYPE', '')

if iskaggle:
    !pip install -Uqq fastbook

# ignore warnings. warnings will disappear if you run this cell a second time

"""# CNN for Diabetic Retinopathy Classification

Diabetic Retinopathy (DR) is a complication of diabetes that damages blood vessel networks in the retina. Diagnosis by color fundus images involves skilled clinicians to recognize the presence of lesions in the image that can be used to detect the disease properly, making it a time-consuming process.

Here I create a convolutional neural network (CNN) to classify retinal fundus images as No DR, Mild Non-Proliferative DR, Moderate Non-Proliferative DR, Severe Non-Proliferative DR, and Proliferative DR.

I use the [Messiador](https://www.adcis.net/en/third-party/messidor/) dataset, which consists of 1,200 labeld retinal fundus images. Here I am fine-tuning *resnet-50* for the classification
"""

pip install fastbook

from google.colab import drive
drive.mount('/content/drive')

from fastbook import *
from PIL import Image as PImage

path = "/content/drive/MyDrive/PBL V GRP 1_3/code/Messidor-2+EyePac_Balanced/"
list_folders =os.listdir(path)

"""This is what the images look like"""

imgpath = path+'0/'
imageList = os.listdir(imgpath)
PImage.open(imgpath + imageList[0])

dls = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=[Resize(300, method='squish')]
).dataloaders(path, bs=32)

dls.show_batch(max_n=6)

learn = vision_learner(dls, resnet50, metrics=error_rate)
learn.fine_tune(3)

learn.export('model.pkl')

"""## Evaluation

Plotting the confusion matrix, we can see the classifier struggles the most with classifications 0-2, and performs significantly better with classes 3 and 4.
"""

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

interp.plot_top_losses(5,nrows=1)

