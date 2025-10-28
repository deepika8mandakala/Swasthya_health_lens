# ==============================================================================
# Swasthya AI - Single-File Backend (Corrected Path)
# This file contains the Flask API, ML model training logic, and food database.
# ==============================================================================

import os
import re
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# --- 1. FLASK APPLICATION SETUP ---
app = Flask(__name__)
CORS(app)

# --- 2. GLOBAL VARIABLES & CONFIGURATION ---
MODEL_FILE_PATH = 'health_risk_model.pkl'
# --- THIS IS THE CORRECTED LINE ---
# It now looks one directory up (../) from where the script is located.
DATASET_FILE_PATH = '../health_dataset_india_2000.csv' 
health_model = None

RISK_CATEGORIES = [
    'Type-2-Diabetes', 'Hypertension', 'Cardiovascular-Disease',
    'Obesity-related-illnesses', 'Chronic-Kidney-Disease',
    'Non-alcoholic-Fatty-Liver-Disease', 'Dyslipidemia-related-risk',
    'Gastrointestinal-disorders', 'Osteoporosis', 'Anemia'
]

# ==============================================================================
# --- 3. MACHINE LEARNING MODEL TRAINING LOGIC ---
# ==============================================================================

def train_new_model():
    """
    Trains a new machine learning model from the dataset.
    """
    print("🤖 Training a new Health Risk Prediction Model...")

    if not os.path.exists(DATASET_FILE_PATH):
        print(f"❌ FATAL ERROR: Dataset not found at the expected path: '{DATASET_FILE_PATH}'")
        print("   Please ensure 'health_dataset_india_2000.csv' is in your main project folder.")
        return None

    df = pd.read_csv(DATASET_FILE_PATH)
    print(f"✅ Dataset loaded successfully with {len(df)} records.")

    encoders = {}
    for col in ['gender', 'activity_level', 'diet_pattern', 'snack_freq', 'smoking_status']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le

    feature_columns = [
        'age', 'gender', 'height_cm', 'weight_kg', 'bmi', 'waist_cm',
        'activity_level', 'diet_pattern', 'meals_per_day', 'snack_freq',
        'water_l_per_day', 'sleep_h', 'smoking_status', 'alcohol_units_week',
        'family_history_diabetes', 'family_history_heart', 'bp_sys', 'bp_dia',
        'fasting_glucose_mg_dl', 'cholesterol_total_mg_dl'
    ]
    
    X = df[feature_columns].fillna(df[feature_columns].median())

    y_data = {category: [] for category in RISK_CATEGORIES}
    for _, row in df.iterrows():
        scores = {pair.split(':')[0].strip(): float(pair.split(':')[1].strip())
                  for pair in row['risk_scores'].split(';') if ':' in pair}
        for category in RISK_CATEGORIES:
            y_data[category].append(scores.get(category, 0.1))

    y = np.array(list(y_data.values())).T

    print("⏳ Training RandomForestRegressor model...")
    model = RandomForestRegressor(
        n_estimators=100, max_depth=10, min_samples_leaf=5,
        random_state=42, n_jobs=-1
    )
    model.fit(X, y)
    print("✅ Model training complete.")

    joblib.dump(model, MODEL_FILE_PATH)
    print(f"💾 Model saved to '{MODEL_FILE_PATH}'.")
    return model

# ==============================================================================
# --- 4. FOOD DATABASE & NUTRITION ANALYSIS ---
# ==============================================================================

FOOD_DATABASE = {
    'rice': {'carbs': 0.78, 'protein': 0.07, 'fat': 0.01, 'calories': 130},
    'roti': {'carbs': 0.45, 'protein': 0.12, 'fat': 0.02, 'calories': 120},
    'chapati': {'carbs': 0.45, 'protein': 0.12, 'fat': 0.02, 'calories': 120},
    'dal': {'carbs': 0.20, 'protein': 0.25, 'fat': 0.01, 'calories': 120},
    'chicken curry': {'carbs': 0.05, 'protein': 0.20, 'fat': 0.12, 'calories': 180},
    'vegetable curry': {'carbs': 0.10, 'protein': 0.05, 'fat': 0.08, 'calories': 130},
    'salad': {'carbs': 0.05, 'protein': 0.02, 'fat': 0.01, 'calories': 30},
    'paneer': {'carbs': 0.02, 'protein': 0.18, 'fat': 0.20, 'calories': 265},
    'egg': {'carbs': 0.01, 'protein': 0.13, 'fat': 0.11, 'calories': 155},
    'poha': {'carbs': 0.75, 'protein': 0.07, 'fat': 0.01, 'calories': 110},
    'tea': {'carbs': 0.00, 'protein': 0.00, 'fat': 0.00, 'calories': 2},
    'water': {'carbs': 0.00, 'protein': 0.00, 'fat': 0.00, 'calories': 0},
}

def analyze_food_items(food_text: str, portion_size: str = 'medium'):
    items = re.split(r'[,&\n]| and ', food_text.lower())
    cleaned_items = [re.sub(r'^\d+\s*', '', item.strip()) for item in items if item.strip()]
    matches = [food for food in cleaned_items if food in FOOD_DATABASE]
    
    portion_multipliers = {'small': 0.75, 'medium': 1.0, 'large': 1.5}
    multiplier = portion_multipliers.get(portion_size, 1.0)

    totals = {'calories': 0, 'protein_g': 0, 'carbs_g': 0, 'fat_g': 0}
    for item in matches:
        serving_size_g = 150
        totals['calories'] += FOOD_DATABASE[item]['calories'] * multiplier * (serving_size_g / 100)
        totals['protein_g'] += FOOD_DATABASE[item]['protein'] * multiplier * serving_size_g
        totals['carbs_g'] += FOOD_DATABASE[item]['carbs'] * multiplier * serving_size_g
        totals['fat_g'] += FOOD_DATABASE[item]['fat'] * multiplier * serving_size_g

    return {
        'found_items': matches,
        'estimated_nutrition': {k: round(v, 1) for k, v in totals.items()}
    }

# ==============================================================================
# --- 5. FLASK API ENDPOINTS ---
# ==============================================================================

def calculate_bmi(height, weight):
    if not height or not weight or height == 0: return 22.5
    return weight / ((height / 100) ** 2)

@app.route('/api/analyze-meal', methods=['POST'])
def analyze_meal_endpoint():
    if not health_model:
        return jsonify({'error': 'Model is not loaded. Cannot process request.'}), 503

    try:
        data = request.get_json()
        if not data: return jsonify({'error': 'Invalid JSON data provided.'}), 400

        feature_vector = np.array([[
            data.get('age', 30),
            1 if data.get('gender') == 'male' else 0,
            data.get('height', 170), data.get('weight', 70),
            calculate_bmi(data.get('height'), data.get('weight')),
            data.get('height', 170) * 0.48, 2, 6, 3, 2,
            2.5, data.get('sleep', 7), 1, 0,
            1 if 'diabetes' in data.get('conditions', []) else 0,
            1 if 'heart-problems' in data.get('conditions', []) else 0,
            120, 80, 90, 180
        ]])

        predictions = health_model.predict(feature_vector)[0]
        risk_predictions = {category: max(0, min(1, predictions[i]))
                            for i, category in enumerate(RISK_CATEGORIES)}

        avg_risk = np.mean(list(risk_predictions.values()))
        health_score = int((1 - avg_risk) * 100)
        
        food_analysis = analyze_food_items(data.get('food-items', ''), data.get('portion-size', 'medium'))
        recommendations = ["Maintain a balanced diet.", "Stay hydrated.", "Engage in regular physical activity."]
        key_insights = f"Your meal has a health score of {health_score}/100. " + \
                       ("Great choice!" if health_score > 75 else "Consider adding more greens.")

        return jsonify({
            'health_score': health_score, 'risk_predictions': risk_predictions,
            'recommendations': recommendations, 'key_insights': key_insights,
            'food_analysis': food_analysis,
        })

    except Exception as e:
        print(f"❌ Error in /api/analyze-meal: {e}")
        return jsonify({'error': 'An internal server error occurred.'}), 500

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': health_model is not None})

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Swasthya AI Backend API!', 'version': '1.0.1'})

# ==============================================================================
# --- 6. APPLICATION STARTUP ---
# ==============================================================================
if __name__ == '__main__':
    if os.path.exists(MODEL_FILE_PATH):
        print("✅ Loading pre-trained model...")
        health_model = joblib.load(MODEL_FILE_PATH)
        print("✅ Model loaded successfully.")
    else:
        health_model = train_new_model()

    if health_model:
        print("🚀 Starting Flask server on http://127.0.0.1:5000")
        app.run(debug=True, port=5000)
    else:
        print("❌ Could not start the server because the model failed to load or train.")