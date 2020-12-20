import os
import string
import random
import json
import requests
import numpy as np
import tensorflow as tf
import PIL.Image
import functools
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

contentPath, stylePath = '', ''
modelUri = f"http://tf_serve:8501/v1/models/tftransfer:predict"
outputDir = './static/temp'

# region functions
def generate_filename():
	"""Generates a random file name with a timestamp."""
	theString = datetime.now().strftime("%Y%m%d_%H%M%S_") + ''.join(random.choices(string.ascii_lowercase, k=5)) 
	return theString + '.jpg'

def tensor_to_image(tensor):
	"""Convert the tensor response to a PIL image."""
	tensor = tensor*255
	tensor = np.array(tensor, dtype=np.uint8)
	if np.ndim(tensor) > 3:
		assert tensor.shape[0] == 1
		tensor = tensor[0]
	return PIL.Image.fromarray(tensor)

def load_img(imgPath):
	"""Load an image for the DNN model."""
	max_dim = 512
	img = tf.io.read_file(imgPath)
	img = tf.image.decode_image(img, channels=3)
	img = tf.image.convert_image_dtype(img, tf.float32)
	
	shape = tf.cast(tf.shape(img)[:-1], tf.float32)
	long_dim = max(shape)
	scale = max_dim / long_dim
	
	new_shape = tf.cast(shape * scale, tf.int32)
	
	img = tf.image.resize(img, new_shape)
	img = img[tf.newaxis, :]
	return img

def get_result(contentPath, stylePath, resultPath):
	"""Get the result."""
	contentImage = load_img(contentPath)
	styleImage = load_img(stylePath)
	contentImage = contentImage.numpy().tolist()
	styleImage = styleImage.numpy().tolist()
	data = json.dumps({
		'inputs': {
			'placeholder': contentImage,
			'placeholder_1': styleImage
		}
	})
	response = requests.post(modelUri, data=data.encode())
	response = response.json()
	data = np.array(response['outputs'], dtype='float32')
	img = tensor_to_image(data)
	img.save(resultPath)
# endregion functions

# region routes
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		uploaded_file1 = request.files['file1']
		uploaded_file2 = request.files['file2']
		if (uploaded_file1.filename != '') and (uploaded_file2.filename != '') and (uploaded_file1.filename[-3:] in ['jpg', 'png']) and (uploaded_file2.filename[-3:] in ['jpg', 'png']):
			contentPath = os.path.join(outputDir, generate_filename())
			stylePath = os.path.join(outputDir, generate_filename())
			resultPath = os.path.join(outputDir, generate_filename())
			uploaded_file1.save(contentPath)
			uploaded_file2.save(stylePath)
			get_result(contentPath, stylePath, resultPath)
			result = {
				'contentPath': contentPath,
				'stylePath': stylePath,
				'resultPath': resultPath
			}
			return render_template('show.html', result=result)
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')
# endregion routes

# region main
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
# endregion main