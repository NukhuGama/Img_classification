import numpy as np
from PIL import Image
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
import cv2 as cv

# Load the Keras model
model = tf.keras.models.load_model('ml_models/my_model.h5')

# Load labels
with open('ml_models/labels.txt', 'r') as f:
    labels = [line.strip() for line in f.readlines()]

def login(request):
    return render(request, 'index.html')



def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'index11.html')


def preprocess_image(img_file):
    # Open and convert image to RGB (PIL)
    image = Image.open(img_file).convert('RGB')

    # Convert to NumPy array
    image_np = np.array(image)

    # Resize image
    input_shape = (120, 120)  # adjust to match your model input
    resized_img = cv.resize(image_np, input_shape, interpolation=cv.INTER_AREA)

    # Normalize and convert to float32
    normalized_img = resized_img / 255.0
    normalized_img = normalized_img.astype(np.float32)

    # Add batch dimension
    input_tensor = np.expand_dims(normalized_img, axis=0)

    return input_tensor

def predict(img_tensor):
    predictions = model.predict(img_tensor)
    class_id = int(np.argmax(predictions))
    confidence = float(predictions[0][class_id])
    return labels[class_id], confidence


def predict_image(request):
    context = {}
    if request.method == 'POST' and 'image' in request.FILES:
        img_file = request.FILES['image']
        print(f"Received file: {img_file.name}")

        # Save uploaded image to media folder
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        file_url = fs.url(filename)

        # Use file from request directly for preprocessing
        input_tensor = preprocess_image(img_file)

        # Predict
        class_name, confidence = predict(input_tensor)
        print(f"Prediction: {class_name}, Confidence: {confidence}")

        # Pass to template
        context = {
            'image_url': file_url,
            'class_name': class_name,
            'confidence': round(confidence * 100, 2),
        }

    return render(request, 'index.html', context)

