from PIL import Image
from urllib import request
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from skimage.metrics import structural_similarity as ssim
import tensorflow as tf
import numpy as np
import os
import glob
from object_detection.utils import visualization_utils as vis_util
from object_detection.utils import label_map_util
from object_detection.utils import ops as utils_ops

STATIC_DIR = os.path.abspath('./webapp/static')
TEMPLATE_DIR = os.path.abspath('./webapp/templates')

app = Flask(__name__, static_url_path='', static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

app.config['UPLOAD_FOLDER'] = "./webapp/static/upload/"
output_folder = './webapp/static/output'


model = tf.saved_model.load(r"E:\fyp\Work\inference_graph\saved_model")
category_index = label_map_util.create_categories_from_labelmap(r'E:\fyp\Work\code\training\labelmap.pbtxt', use_display_name=True)


##inference and visualize part based on tensorflow 2 object detection api tutorial 
##https://github.com/tensorflow/models/blob/master/research/object_detection/colab_tutorials/object_detection_tutorial.ipynb
def inference_on_image(image):
    image = np.asarray(image)
    input = tf.convert_to_tensor(image)
    input = input[tf.newaxis,...]

    model_fn = model.signatures['serving_default']
    output = model_fn(input)
    num_detections = int(output.pop('num_detections'))
    output = {key:value[0, :num_detections].numpy() 
                 for key,value in output.items()}
    output['num_detections'] = num_detections
    output['detection_classes'] = output['detection_classes'].astype(np.int64)
   
    if 'detection_masks' in output:
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
              output['detection_masks'], output['detection_boxes'],
               image.shape[0], image.shape[1])      
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.2,
                                       tf.uint8)
        output['detection_masks_reframed'] = detection_masks_reframed.numpy()
    
    return output



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['GET','POST'])
def upload_file():
    nameOfFiles = []
    files = request.files.getlist('files[]')
    count = 0
    result_list = []
    contain_bbox = []
    bool_anyone_have_detection = False

    for file in glob.glob(r"E:\fyp\Work\code\webapp\static\output\*"):
        os.remove(file)

    for file in files:
        name = secure_filename(file.filename)
        nameOfFiles.append(name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))

##inference and visualize part based on tensorflow 2 object detection api tutorial 
##https://github.com/tensorflow/models/blob/master/research/object_detection/colab_tutorials/object_detection_tutorial.ipynb
    for image in glob.glob("./webapp/static/upload/*.jpg"):
        bool_contain_bbox = False
        img = np.array(Image.open(image))
        inference = inference_on_image(img)

        vis_util.visualize_boxes_and_labels_on_image_array(
            img,
            inference['detection_boxes'],
            inference['detection_classes'],
            inference['detection_scores'],
            category_index[0],
            min_score_thresh=0.25,
            instance_masks=inference.get('detection_masks_reframed', None),
            use_normalized_coordinates=True,
            line_thickness=8,
            skip_labels=True)
        
        result = Image.fromarray(img)       
        result.save(fr'E:\fyp\Work\code\webapp\static\output\{count}.jpg')
        count = count + 1

        pre = np.array(Image.open(image))
        post = np.array(result)

        ssim_score = ssim(pre, post, multichannel=True)
        if ssim_score == 1.0:
            contain_bbox.append(bool_contain_bbox)
        else:
            bool_contain_bbox = True
            contain_bbox.append(bool_contain_bbox)
    
    bool_anyone_have_detection = any(contain_bbox)
        
    for file in glob.glob("./webapp/static/upload/*"):
        os.remove(file)

    resultDir = os.listdir(output_folder)
    resultDir = sorted(resultDir,key=lambda x: int(os.path.splitext(x)[0]))
    for result_file in resultDir:
        result_list.append(result_file)
    
    return render_template('result.html', result_list=result_list, contain_bbox=contain_bbox, bool_anyone_have_detection=bool_anyone_have_detection)


if __name__ == '__main__':
    ##app.debug = True
    app.run()