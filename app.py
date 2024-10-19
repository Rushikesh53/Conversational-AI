from flask import Flask, request, render_template, jsonify
import os
from model import ImageRecognitionModel

app = Flask(__name__)
model = ImageRecognitionModel()

# Create uploads directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Classify the image
    try:
        class_name = model.classify_image(file_path)
        return jsonify({'class_name': class_name})
    except Exception as e:
        return jsonify({'error': str(e)})

# Corrected main check
if __name__ == '__main__':
    app.run(debug=True)
