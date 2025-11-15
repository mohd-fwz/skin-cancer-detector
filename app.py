from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_example_images():
    """Get list of example images from the examples folder"""
    examples_folder = os.path.join('static', 'images', 'examples')
    if os.path.exists(examples_folder):
        images = [f for f in os.listdir(examples_folder) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        return sorted(images)  # Sort alphabetically
    return []

# Routes
@app.route('/')
def home():
    example_images = get_example_images()
    return render_template('home.html', example_images=example_images)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # This will be used for image upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'success': True, 'filename': filename}), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/predict', methods=['POST'])
def predict():
    # This will be connected to your model later
    # For now, we'll return dummy data
    return jsonify({
        'prediction': 'Melanocytic nevi (nv)',
        'probability': 0.85,
        'confidence': 'high',
        'heatmap': 'path/to/heatmap.png'
    })

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)