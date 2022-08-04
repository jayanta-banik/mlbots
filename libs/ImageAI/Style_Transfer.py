import cv2
import string
import random
import numpy as np
import pandas as pd
from PIL import Image
import tflite_runtime.interpreter as tflite


style_predict_path = 'models/StyleTransfer/lite-model_arbitrary-image-stylization-256_int8_predict_1.tflite'
style_transform_path = 'models/StyleTransfer/lite-model_arbitrary-image-stylization-256_int8_transfer_1.tflite'

load_img = lambda path: cv2.cvtColor(cv2.imread(path, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGR2RGB)
resize_image = lambda image, target_dim: cv2.resize(image, [target_dim, target_dim], interpolation = cv2.INTER_AREA)
preprocess = lambda imgs: np.array([imgs], dtype=np.float32)/255
randStr = lambda N=7 : ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))

# Function to run style prediction on preprocessed style image.
def run_style_predict(preprocessed_style_image):
    # Load the model.
    interpreter = tflite.Interpreter(model_path=style_predict_path)

    # Set model input.
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]["index"], preprocessed_style_image)

    # Calculate style bottleneck.
    interpreter.invoke()
    style_bottleneck = interpreter.tensor(
      interpreter.get_output_details()[0]["index"]
      )()

    return style_bottleneck

# Run style transform on preprocessed style image
def run_style_transform(style_bottleneck, preprocessed_content_image):
    # Load the model.
    interpreter = tflite.Interpreter(model_path=style_transform_path)

    # Set model input.
    input_details = interpreter.get_input_details()
    interpreter.allocate_tensors()

    # Set model inputs.
    interpreter.set_tensor(input_details[0]["index"], preprocessed_content_image)
    interpreter.set_tensor(input_details[1]["index"], style_bottleneck)
    interpreter.invoke()

    # Transform content image.
    stylized_image = interpreter.tensor(
      interpreter.get_output_details()[0]["index"]
      )()

    return stylized_image

def applyTransfer(uri_for_content, uri_for_style, content_blending_ratio=0.5):
  preprocessed_content_image = preprocess(resize_image(load_img(uri_for_content), 384))
  preprocessed_style_image = preprocess(resize_image(load_img(uri_for_style), 256))
  
  style_bottleneck = run_style_predict(preprocessed_style_image)
  style_bottleneck_content = run_style_predict(preprocess(resize_image(load_img(uri_for_content), 256)))
  
  style_bottleneck_blended = content_blending_ratio * style_bottleneck_content + (1 - content_blending_ratio) * style_bottleneck
  
  stylized_image_blended = run_style_transform(style_bottleneck_blended, preprocessed_content_image)
  
  im = Image.fromarray((stylized_image_blended[0]*255).astype(np.uint8))

  uri_for_transform = "transformed/" + randStr(4) + uri_for_content.split('/')[-1]
  im.save( "res/" + uri_for_transform)
  print(uri_for_transform)
  return uri_for_transform