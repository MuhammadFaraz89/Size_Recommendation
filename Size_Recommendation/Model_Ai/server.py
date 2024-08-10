from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import os
import subprocess
from werkzeug.utils import secure_filename
from Tshirt import process_upload  # Import the process_upload function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File saved to {filepath}")
        size_result = process_upload(filepath)  # Use process_upload here
        print(f"Predicted size: {size_result}")
        return jsonify({'result': size_result})
    return redirect(request.url)


@app.route('/run-tshirt-script', methods=['POST'])
def run_tshirt_script():
    try:
        result = subprocess.run(['python', os.path.join(os.path.dirname(__file__), 'tshirt.py')],
                                capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-glasses-script', methods=['POST'])
def run_glasses_script():
    try:
        result = subprocess.run(['python', os.path.join(os.path.dirname(__file__), 'new.py')],
                                capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-watch-script', methods=['POST'])
def run_watch_script():
    try:
        result = subprocess.run(['python', os.path.join(os.path.dirname(__file__), 'wrist_detection.py')],
                                capture_output=True, text=True)
        return jsonify({'output': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
