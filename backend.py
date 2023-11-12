from flask import Flask, request, jsonify
from PIL import Image
from keras.models import load_model
from keras.preprocessing import image
import os
import shutil

app = Flask(__name__)

model = load_model('documentClassifierModel.h5')

def preprocess_input_image(input_path, output_path):
   
    with Image.open(input_path) as img:
        img_resized = img.resize((224, 224))
        img_resized.save(output_path)

@app.route('/classify', methods=['POST'])
def classify_documents():
    files = request.files.getlist('files')

    temp_dir = 'temp_images'
    os.makedirs(temp_dir, exist_ok=True)

    categorized_files = {}

    for file in files:
        original_path = os.path.join(temp_dir, file.filename)
        file.save(original_path)

        image_path = os.path.join(temp_dir, f"{file.filename.split('.')[0]}.png")
        preprocess_input_image(original_path, image_path)

        predicted_category = classify_image(image_path)

        category_folder = os.path.join(temp_dir, predicted_category)
        os.makedirs(category_folder, exist_ok=True)
        shutil.move(original_path, category_folder)

        categorized_files.setdefault(predicted_category, []).append(file.filename)

    shutil.rmtree(temp_dir)

    return jsonify(categorized_files)

def classify_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array.reshape((1, 224, 224, 3))
    img_array /= 255.0 

    prediction = model.predict(img_array)
    predicted_class = 'positive' if prediction[0][0] > 0.5 else 'negative'

    return predicted_class

if __name__ == '__main__':
    app.run(debug=True)
