# Skin Cancer Detector

A web-based application that uses deep learning and explainable AI to detect skin cancer types from images.

## 🎯 Overview

This application analyzes skin lesion images using a trained MobileNetV3 neural network model and provides:
- **Cancer type prediction** with confidence scores
- **GradCAM heatmaps** to visualize which parts of the image influenced the prediction
- **AI-generated medical explanations** using Google's Gemini API
- **Patient data collection** for comprehensive analysis

## ✨ Features

- 📸 **Image Upload**: Support for JPG, JPEG, and PNG files (max 5MB)
- 🧠 **ML Predictions**: Detects 7 types of skin lesions:
  - Melanoma
  - Basal Cell Carcinoma
  - Benign Keratosis
  - Dermatofibroma
  - Actinic Keratoses
  - Melanocytic Nevus
  - Vascular Lesion
- 🔥 **Explainability**: GradCAM heatmaps show model decision regions
- 🤖 **AI Explanations**: Gemini-powered medical insights based on patient data
- 📊 **Patient Forms**: Collects age, gender, skin type, symptoms, and medical history

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **ML Model**: TensorFlow/Keras with MobileNetV3
- **Explainability**: GradCAM (Gradient-weighted Class Activation Mapping)
- **AI**: Google Gemini API
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: OpenCV, NumPy

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd skin-cancer-detector
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a .env file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
   
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
├── app.py                      # Flask application & routes
├── model/
│   ├── final_model.keras      # Trained ML model
│   └── prediction.py          # Prediction & GradCAM logic
├── gemini_helper.py           # AI explanation generation
├── templates/                 # HTML templates
├── static/
│   ├── css/                   # Stylesheets
│   ├── js/                    # Frontend scripts
│   ├── images/                # Example & GradCAM images
│   └── uploads/               # User uploaded images
├── requirements.txt           # Python dependencies
└── .env                       # API keys (not in git)
```

## 🔑 Key Files

- app.py - Main Flask application with routes
- prediction.py - ML prediction and GradCAM generation
- gemini_helper.py - Medical explanation AI integration

## 📝 Usage

1. **Upload an image** of a skin lesion
2. **Fill in patient information** (age, gender, location, symptoms, etc.)
3. **Submit the form** to get predictions
4. **View results** including:
   - Predicted cancer type and confidence
   - GradCAM heatmap visualization
   - AI-generated medical explanation

## ⚠️ Disclaimer

This tool is for educational purposes only and should **NOT** be used as a substitute for professional medical diagnosis. Always consult with a qualified dermatologist.

## 👥 Team Members

This project is developed and maintained by our dedicated team:

| [<img src="https://github.com/mohd-fwz.png" width="70" alt="mohd-fwz" style="border-radius:50%;" />](https://github.com/mohd-fwz) | [<img src="https://github.com/Amjuks.png" width="70" alt="Amjuks" style="border-radius:50%;" />](https://github.com/Amjuks) | [<img src="https://github.com/aaradhyasaxena0606.png" width="70" alt="aaradhyasaxena0606" style="border-radius:50%;" />](https://github.com/aaradhyasaxena0606) | [<img src="https://github.com/Pavan-484.png" width="70" alt="Pavan-484" style="border-radius:50%;" />](https://github.com/Pavan-484) |
|---|---|---|---|
| [**mohd-fwz**](https://github.com/mohd-fwz) | [**Amjuks**](https://github.com/Amjuks) | [**aaradhyasaxena0606**](https://github.com/aaradhyasaxena0606) | [**Pavan-484**](https://github.com/Pavan-484) |

---

**⚡ Note**: The model file (final_model.keras) must be trained and placed in the model directory before running the application.