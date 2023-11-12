from flask import Flask, request, jsonify
from PIL import Image
from keras.models import load_model
from keras.preprocessing import image
import os
import shutil

app = Flask(__name__)

# Load the pre-trained model
model = load_model('your_pretrained_model.h5')  # Replace with the path to your model file

def preprocess_input_image(input_path, output_path):
    # Function to convert text or PDF files to images (224x224)

    # Replace this logic with your own for text/PDF to image conversion
    # This is just a placeholder example using PIL to open the file and resize it
    with Image.open(input_path) as img:
        img_resized = img.resize((224, 224))
        img_resized.save(output_path)

@app.route('/classify', methods=['POST'])
def classify_documents():
    files = request.files.getlist('files')

    # Create a temporary directory to store processed images
    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    categorized_files = {}

    for file in files:
        # Save the original file to the temporary directory
        original_path = os.path.join(temp_dir, file.filename)
        file.save(original_path)

        # Convert the file to an image (224x224)
        image_path = os.path.join(temp_dir, f"{file.filename.split('.')[0]}.png")
        preprocess_input_image(original_path, image_path)

        # Use the model to classify the image
        predicted_category = classify_image(image_path)

        # Move the file to the corresponding category folder
        category_folder = os.path.join(temp_dir, predicted_category)
        os.makedirs(category_folder, exist_ok=True)
        shutil.move(original_path, category_folder)

        categorized_files.setdefault(predicted_category, []).append(file.filename)

    # Remove the temporary directory
    shutil.rmtree(temp_dir)

    return jsonify(categorized_files)

def classify_image(image_path):
    # Implement your model prediction logic here
    # This is a placeholder example assuming a binary classification
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array.reshape((1, 224, 224, 3))
    img_array /= 255.0  # Normalize the image array

    prediction = model.predict(img_array)
    predicted_class = 'positive' if prediction[0][0] > 0.5 else 'negative'

    return predicted_class

if __name__ == '__main__':
    app.run(debug=True)
