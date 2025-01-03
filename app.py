from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import io

app = Flask(__name__)

# Load the pre-trained model
model = load_model('Blood_Group_Mode3.h5')
blood_groups = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']

def classify_image(image):
    input_image = image.resize((180, 180))  # Resize to model input size
    input_image_array = np.array(input_image) / 255.0
    input_image_array = np.expand_dims(input_image_array, axis=0)  # Add batch dimension
    predictions = model.predict(input_image_array)
    predicted_class = np.argmax(predictions, axis=1)
    confidence = predictions[0][predicted_class[0]]
    return blood_groups[predicted_class[0]], confidence

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    
    # Read and preprocess the image
    image = Image.open(io.BytesIO(file.read())).convert("RGB")
    
    # Get prediction
    predicted_group, confidence = classify_image(image)
    
    return jsonify({
        'blood_group': predicted_group,
        'confidence': f"{confidence:.2%}"
    })

if __name__ == '__main__':
    app.run(debug=True)
