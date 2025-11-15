from flask import Flask, render_template, request, jsonify
import os
import json
import random
from werkzeug.utils import secure_filename
from dotenv import load_dotenv 
from gemini_helper import generate_medical_explanation
from model.prediction import predict_with_gradcam

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['GRADCAM_FOLDER'] = 'static/images/gradcam'  # New folder for GradCAM images
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
        return sorted(images)
    return []

# ============================================
# DUMMY ML MODEL (Temporary - for testing)
# ============================================

def dummy_ml_prediction(uploaded_filename):
    """
    Simulate ML model prediction
    This will be replaced by your friend's actual model
    
    Returns dummy predictions for testing
    """
    
    # List of possible cancer types
    cancer_types = [
        {'name': 'Melanoma (mel)', 'risk': 'high'},
        {'name': 'Melanocytic Nevi (nv)', 'risk': 'low'},
        {'name': 'Basal Cell Carcinoma (bcc)', 'risk': 'moderate'},
        {'name': 'Actinic Keratoses (akiec)', 'risk': 'moderate'},
        {'name': 'Benign Keratosis (bkl)', 'risk': 'low'},
        {'name': 'Dermatofibroma (df)', 'risk': 'low'},
        {'name': 'Vascular Lesions (vasc)', 'risk': 'low'}
    ]
    
    # Randomly select a cancer type (for demo purposes)
    selected = random.choice(cancer_types)
    
    # Generate random probability based on risk level
    if selected['risk'] == 'high':
        probability = random.uniform(0.70, 0.95)
    elif selected['risk'] == 'moderate':
        probability = random.uniform(0.50, 0.75)
    else:
        probability = random.uniform(0.60, 0.85)
    
    return {
        'cancer_type': selected['name'],
        'probability': round(probability, 2),
        'confidence': 'high' if probability > 0.75 else 'moderate' if probability > 0.50 else 'low'
    }

# ============================================
# ROUTES
# ============================================

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
    """Handle image upload"""
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
    """
    Handle prediction request
    Collects form data, gets ML prediction, generates AI explanation
    """
    
    try:
        # ============================================
        # 1. COLLECT PATIENT DATA FROM FORM
        # ============================================
        
        patient_data = {
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'skin_type': request.form.get('skinType'),
            'location': request.form.get('location'),
            'lesion_size': request.form.get('lesionSize'),
            'duration': request.form.get('duration'),
            'family_history': request.form.get('familyHistory'),
            'sun_exposure': request.form.get('sunExposure'),
            'symptoms': request.form.get('symptoms'),  # This is a JSON string
            'additional_notes': request.form.get('additionalNotes')
        }
        
        # Get uploaded filename
        uploaded_file = request.files.get('file')
        filename = uploaded_file.filename if uploaded_file else None
        
        # ============================================
        # 2. GET ML MODEL PREDICTION WITH GRADCAM
        # ============================================
        
        if uploaded_file and filename:
            # Save the uploaded file temporarily
            filename = secure_filename(filename)
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(upload_path)
            
            # Get prediction with GradCAM
            model_result = predict_with_gradcam(upload_path)
            
            # Copy GradCAM image to static/images/gradcam folder
            if os.path.exists(model_result['gradcam_path']):
                gradcam_filename = os.path.basename(model_result['gradcam_path'])
                destination_path = os.path.join(app.config['GRADCAM_FOLDER'], gradcam_filename)
                
                # Ensure destination directory exists
                os.makedirs(app.config['GRADCAM_FOLDER'], exist_ok=True)
                
                # Copy the GradCAM image
                import shutil
                shutil.copy(model_result['gradcam_path'], destination_path)
                
                prediction = {
                    'cancer_type': model_result['prediction'],
                    'probability': model_result['confidence'],
                    'confidence': 'high' if model_result['confidence'] > 0.75 else 'moderate' if model_result['confidence'] > 0.50 else 'low'
                }
                gradcam_url = f'/static/images/gradcam/{gradcam_filename}'
            else:
                raise Exception("GradCAM image generation failed")
        else:
            raise Exception("No file uploaded for prediction")
        
        # ============================================
        # 3. GENERATE AI EXPLANATION USING GEMINI
        # ============================================
        
        ai_explanation = generate_medical_explanation(patient_data, prediction)
        
        # ============================================
        # 4. RETURN RESULTS TO FRONTEND
        # ============================================
        
        return jsonify({
            'success': True,
            'prediction': prediction['cancer_type'],
            'probability': prediction['probability'],
            'confidence': prediction['confidence'],
            'explanation': ai_explanation,
            'heatmap': gradcam_url
        })
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create necessary folders if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['GRADCAM_FOLDER'], exist_ok=True)
    app.run(debug=True, port=5000)