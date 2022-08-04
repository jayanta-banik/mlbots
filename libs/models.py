import cv2
import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite
from flask import Flask, flash, redirect, render_template, jsonify, request, send_from_directory, url_for, flash
import json

def classify_image():
	image = request.get_json(force=True)['image']
	image = cv2.imread(image)
	with open("models/labels_photo_classification.txt") as file:
	    labels = file.read().split('\n')

	interpreter = tflite.Interpreter(model_path='models/photo_classification.tflite')
	model_intput = interpreter.get_input_details()[0]
	model_output = interpreter.get_output_details()[0]

	stretch_near =np.array([cv2.resize(image, (224, 224), interpolation = cv2.INTER_NEAREST)])
	interpreter.allocate_tensors()
	interpreter.set_tensor(model_intput['index'], stretch_near)
	interpreter.invoke()
	y = list(interpreter.get_tensor(model_output['index'])[0])

	df = pd.DataFrame()
	df['labels'] = labels
	df['values'] = y
	df.sort_values(by='values', ascending=False, inplace=True)
	data = {
		    "match":df.iloc[0].values.tolist(),
		    "possible_match":df.iloc[1:6].values.tolist()
		}
	return str(data)