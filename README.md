# Cityu-FYP-21CS090-Computer-vision-and-Web-app-for-marine-mammels

## Dataset from https://data.ncl.ac.uk/collections/The_Northumberland_Dolphin_Dataset_2020/4982342/1

# RUNNING WEBAPP
### 1. To run the webapp, first make sure these python library was installed beforehand:
- from PIL import Image
- from urllib import request
- from flask import Flask, render_template, request
- from werkzeug.utils import secure_filename
- from skimage.metrics import structural_similarity as ssim
- import tensorflow as tf
- import numpy as np
- import os
- import glob
- from object_detection.utils import visualization_utils as vis_util
- from object_detection.utils import label_map_util
- from object_detection.utils import ops as utils_ops

### 2. Then change line 23,24 to point at where you would like to place the model
### 3. As well as line 67 and 95 at where you would like to put the output directory

### 4. Finally use command line console to get to where app.py is at and type "python app.py" to execute
