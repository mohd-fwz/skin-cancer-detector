import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
# ============================================
# GEMINI API CONFIGURATION
# ============================================

# Configure Gemini API
# You can use environment variable or direct key
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set! Please create a .env file.")

genai.configure(api_key=API_KEY)

# Use Gemini 2.5 Flash (stable and fast)
model = genai.GenerativeModel('gemini-2.5-flash')

# ============================================
# MAIN FUNCTION
# ============================================

def generate_medical_explanation(patient_data, prediction):
    """
    Generate medical explanation using Gemini API
    
    Args:
        patient_data: Dictionary containing patient information from the form
            - age, gender, skin_type, location, lesion_size, duration, 
              family_history, sun_exposure, symptoms, additional_notes
        
        prediction: Dictionary containing ML model prediction
            - cancer_type: String (e.g., "Melanoma (mel)")
            - probability: Float (e.g., 0.87 for 87%)
    
    Returns:
        String with AI-generated medical explanation
    """
    
    # Format symptoms list
    symptoms_list = patient_data.get('symptoms', [])
    if isinstance(symptoms_list, str):
        # If it's a JSON string, parse it
        import json
        try:
            symptoms_list = json.loads(symptoms_list)
        except:
            symptoms_list = []
    
    symptoms_text = ", ".join(symptoms_list) if symptoms_list else "None reported"
    
    # Create prompt for Gemini
    prompt = f"""
You are a medical AI assistant helping explain skin cancer detection results. Based on the following information, provide a clear, professional, and empathetic explanation for the patient.

PATIENT INFORMATION:
- Age: {patient_data.get('age', 'Not provided')} years
- Gender: {patient_data.get('gender', 'Not provided')}
- Skin Type: {patient_data.get('skin_type', 'Not provided')}
- Lesion Location: {patient_data.get('location', 'Not provided')}
- Lesion Size: {patient_data.get('lesion_size', 'Not provided')}
- Duration: {patient_data.get('duration', 'Not provided')}
- Family History of Skin Cancer: {patient_data.get('family_history', 'Not provided')}
- Sun Exposure Level: {patient_data.get('sun_exposure', 'Not provided')}
- Symptoms: {symptoms_text}
{f"- Additional Notes: {patient_data.get('additional_notes')}" if patient_data.get('additional_notes') else ""}

AI MODEL PREDICTION:
- Detected Type: {prediction['cancer_type']}
- Confidence Level: {prediction['probability']*100:.1f}%

INSTRUCTIONS:
1. Explain what {prediction['cancer_type']} is in simple terms (2-3 sentences)
2. Explain why the AI model detected this based on the patient's specific characteristics and symptoms
3. Mention relevant risk factors from the patient's profile
4. Provide next steps and recommendations
5. Keep the tone professional but empathetic
6. Remind them this is preliminary and they MUST see a dermatologist

Keep the response under 250 words. Be clear and concise.
"""
    
    try:
        # Generate response from Gemini
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # Fallback response if API fails
        return f"We detected {prediction['cancer_type']} with {prediction['probability']*100:.1f}% confidence. However, we're unable to generate a detailed explanation at this time. Please consult a dermatologist immediately for proper diagnosis and treatment."

# ============================================
# TEST FUNCTION (Optional)
# ============================================

if __name__ == "__main__":
    # Test with dummy data
    test_patient = {
        'age': 45,
        'gender': 'Male',
        'skin_type': 'Type II - Fair',
        'location': 'Back',
        'lesion_size': 'Medium (5-10mm)',
        'duration': 'Few months (1-6 months)',
        'family_history': 'Yes',
        'sun_exposure': 'High',
        'symptoms': ['Changing color', 'Growing in size'],
        'additional_notes': 'Noticed after summer vacation'
    }
    
    test_prediction = {
        'cancer_type': 'Melanoma (mel)',
        'probability': 0.87
    }
    
    print("Testing Gemini Helper...\n")
    explanation = generate_medical_explanation(test_patient, test_prediction)
    print("Generated Explanation:")
    print("=" * 60)
    print(explanation)
    print("=" * 60)