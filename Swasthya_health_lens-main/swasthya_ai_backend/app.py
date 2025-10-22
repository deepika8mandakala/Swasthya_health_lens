from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import re
from food_database import FOOD_DATABASE, analyze_food_items
from simple_train_model import create_simple_model
import os

app = Flask(__name__)
CORS(app)

# Global variables for models
health_model = None
risk_categories = [
    'Type-2-Diabetes', 'Hypertension', 'Cardiovascular-Disease',
    'Obesity-related-illnesses', 'Chronic-Kidney-Disease',
    'Non-alcoholic-Fatty-Liver-Disease', 'Dyslipidemia-related-risk',
    'Gastrointestinal-disorders', 'Osteoporosis', 'Anemia'
]

def load_model():
    """Load the trained health risk prediction model"""
    global health_model
    try:
        if os.path.exists('health_risk_model.pkl'):
            health_model = joblib.load('health_risk_model.pkl')
            print("Model loaded successfully")
        else:
            print("Model file not found. Training new model...")
            train_new_model()
    except Exception as e:
        print(f"Error loading model: {e}")
        train_new_model()

def train_new_model():
    """Train a new model if loading fails"""
    global health_model
    try:
        model = create_simple_model()
        if model:
            health_model = model
            print("New model trained and loaded successfully")
        else:
            print("Failed to train model")
            health_model = None
    except Exception as e:
        print(f"Error training model: {e}")
        health_model = None

def calculate_bmi(height, weight):
    """Calculate BMI from height and weight"""
    height_m = height / 100
    return weight / (height_m ** 2)

def encode_categorical_features(data):
    """Encode categorical features for model prediction"""
    # Activity level encoding
    activity_mapping = {
        'sedentary': 0, 'light': 1, 'moderate': 2, 'active': 3, 'very-active': 4
    }
    data['activity_level_encoded'] = activity_mapping.get(data.get('activity-level', 'moderate'), 2)
    
    # Gender encoding
    gender_mapping = {'male': 1, 'female': 0, 'other': 0.5}
    data['gender_encoded'] = gender_mapping.get(data.get('gender', 'male'), 1)
    
    # Diet pattern encoding (simplified)
    diet_mapping = {
        'vegetarian': 0, 'non-vegetarian': 1, 'eggetarian': 0.5,
        'lacto-vegetarian': 0.3, 'north-indian': 0.7
    }
    data['diet_pattern_encoded'] = diet_mapping.get(data.get('diet-pattern', 'vegetarian'), 0)
    
    # Water intake encoding
    water_mapping = {
        'less-than-1l': 0.5, '1-2l': 1.5, '2-3l': 2.5, 'more-than-3l': 3.5
    }
    data['water_intake_encoded'] = water_mapping.get(data.get('water-intake', '2-3l'), 2.5)
    
    return data

def generate_recommendations(risk_scores, user_data):
    """Generate personalized recommendations based on risk scores and user data"""
    recommendations = []
    
    # High risk recommendations
    high_risk_conditions = [condition for condition, score in risk_scores.items() if score > 0.3]
    
    if 'Type-2-Diabetes' in high_risk_conditions:
        recommendations.append("Reduce refined carbohydrates and added sugars. Focus on whole grains and fiber-rich foods.")
    
    if 'Hypertension' in high_risk_conditions:
        recommendations.append("Limit sodium intake to less than 2g per day. Increase potassium-rich foods like bananas and leafy greens.")
    
    if 'Cardiovascular-Disease' in high_risk_conditions:
        recommendations.append("Increase omega-3 fatty acids through fish, nuts, and seeds. Limit saturated and trans fats.")
    
    if 'Obesity-related-illnesses' in high_risk_conditions:
        recommendations.append("Focus on portion control and regular physical activity. Aim for gradual weight loss of 0.5-1kg per week.")
    
    # General recommendations based on user data
    if user_data.get('activity-level') == 'sedentary':
        recommendations.append("Increase physical activity to at least 150 minutes of moderate exercise per week.")
    
    if user_data.get('sleep', 7) < 6:
        recommendations.append("Improve sleep hygiene: maintain regular sleep schedule and reduce screen time before bed.")
    
    if user_data.get('water-intake') in ['less-than-1l', '1-2l']:
        recommendations.append("Increase water intake to 2-3 liters per day for better hydration.")
    
    # Default recommendations if none generated
    if not recommendations:
        recommendations = [
            "Maintain a balanced diet with plenty of fruits and vegetables.",
            "Stay physically active with regular exercise.",
            "Get adequate sleep (7-8 hours per night).",
            "Stay hydrated by drinking plenty of water."
        ]
    
    return recommendations[:5]  # Limit to 5 recommendations

@app.route('/api/analyze-meal', methods=['POST'])
def analyze_meal():
    """Main API endpoint for meal analysis"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract food items and analyze nutrition
        food_items_text = data.get('food-items', '')
        food_analysis = analyze_food_items(food_items_text)
        
        # Prepare data for health risk prediction
        user_data = encode_categorical_features(data)
        
        # Calculate BMI
        height = user_data.get('height', 170)
        weight = user_data.get('weight', 70)
        bmi = calculate_bmi(height, weight)
        user_data['bmi'] = bmi
        
        # Prepare features for model prediction (simplified)
        features = {
            'age': user_data.get('age', 30),
            'height_cm': height,
            'weight_kg': weight,
            'bmi': bmi,
            'waist_cm': height * 0.45,  # Estimate waist circumference
            'meals_per_day': user_data.get('meals-per-day', 3),
            'water_l_per_day': user_data.get('water_intake_encoded', 2.5),
            'sleep_h': user_data.get('sleep', 7),
            'alcohol_units_week': user_data.get('alcohol', 0),
            'family_history_diabetes': 1 if 'diabetes' in user_data.get('conditions', []) else 0,
            'family_history_heart': 1 if 'heart-problems' in user_data.get('conditions', []) else 0,
            'bp_sys': 120,  # Default normal values
            'bp_dia': 80,
            'fasting_glucose_mg_dl': 90,
            'cholesterol_total_mg_dl': 180
        }
        
        # Predict health risks
        risk_predictions = {}
        if health_model is not None:
            try:
                # Create feature vector in the same order as training (simplified)
                feature_vector = np.array([[
                    features['age'], features['height_cm'], features['weight_kg'],
                    features['bmi'], features['waist_cm'], features['meals_per_day'],
                    features['water_l_per_day'], features['sleep_h'], features['alcohol_units_week'],
                    features['family_history_diabetes'], features['family_history_heart'],
                    features['bp_sys'], features['bp_dia'], features['fasting_glucose_mg_dl'],
                    features['cholesterol_total_mg_dl']
                ]])
                
                # Predict for each risk category
                for i, category in enumerate(risk_categories):
                    if i < health_model.n_outputs_:
                        prediction = health_model.predict(feature_vector)[0][i]
                        risk_predictions[category] = max(0, min(1, prediction))  # Clamp between 0 and 1
                    else:
                        risk_predictions[category] = 0.1  # Default low risk
            except Exception as e:
                print(f"Error in model prediction: {e}")
                # Fallback to default risks
                risk_predictions = {category: 0.1 for category in risk_categories}
        else:
            # Fallback when model is not available
            risk_predictions = {category: 0.1 for category in risk_categories}
        
        # Calculate overall health score
        avg_risk = np.mean(list(risk_predictions.values()))
        health_score = max(0, min(100, int((1 - avg_risk) * 100)))
        
        # Generate recommendations
        recommendations = generate_recommendations(risk_predictions, user_data)
        
        # Generate key insights
        key_insights = f"Health analysis completed. Your meal shows a {health_score}/100 health score. "
        if health_score >= 80:
            key_insights += "Excellent nutritional choices! Keep up the good work."
        elif health_score >= 60:
            key_insights += "Good meal overall. Consider adding more vegetables for better nutrition."
        else:
            key_insights += "This meal could be improved. Focus on whole foods and balanced nutrition."
        
        # Prepare response
        response = {
            'health_score': health_score,
            'food_analysis': food_analysis,
            'risk_predictions': risk_predictions,
            'recommendations': recommendations,
            'key_insights': key_insights
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in analyze_meal: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': health_model is not None,
        'available_endpoints': ['/api/analyze-meal', '/api/health']
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Swasthya AI - Health Analysis API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/analyze-meal': 'Analyze meal and predict health risks',
            'GET /api/health': 'Health check endpoint'
        },
        'usage': {
            'analyze_meal': {
                'method': 'POST',
                'url': '/api/analyze-meal',
                'body': {
                    'food-items': 'string (required)',
                    'meal-type': 'string (required)',
                    'portion-size': 'string (required)',
                    'age': 'number (required)',
                    'gender': 'string (required)',
                    'height': 'number (required)',
                    'weight': 'number (required)',
                    'activity-level': 'string (required)',
                    'conditions': 'array (optional)',
                    'sleep': 'number (optional)',
                    'water-intake': 'string (optional)'
                }
            }
        }
    })

if __name__ == '__main__':
    print("Loading Swasthya AI Health Analysis API...")
    load_model()
    print("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

