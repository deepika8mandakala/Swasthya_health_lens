"""
Simplified Health Risk Prediction Model Training
A more robust version that handles data preprocessing better
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from typing import Dict, List, Tuple

def create_simple_model():
    """Create a simple model that works with the available data"""
    print("Creating simplified health risk prediction model...")
    
    # Load the dataset
    dataset_path = '../health_dataset_india_2000.csv'
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return None
    
    df = pd.read_csv(dataset_path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Select only numeric columns for simplicity
    numeric_columns = [
        'age', 'height_cm', 'weight_kg', 'bmi', 'waist_cm',
        'meals_per_day', 'water_l_per_day', 'sleep_h', 'alcohol_units_week',
        'family_history_diabetes', 'family_history_heart',
        'bp_sys', 'bp_dia', 'fasting_glucose_mg_dl', 'cholesterol_total_mg_dl'
    ]
    
    # Create feature matrix
    X = df[numeric_columns].fillna(df[numeric_columns].median())
    
    # Risk categories
    risk_categories = [
        'Type-2-Diabetes', 'Hypertension', 'Cardiovascular-Disease',
        'Obesity-related-illnesses', 'Chronic-Kidney-Disease',
        'Non-alcoholic-Fatty-Liver-Disease', 'Dyslipidemia-related-risk',
        'Gastrointestinal-disorders', 'Osteoporosis', 'Anemia'
    ]
    
    # Parse risk scores and create target variables
    y_data = {}
    for category in risk_categories:
        y_data[category] = []
    
    for idx, row in df.iterrows():
        risk_scores_str = str(row.get('risk_scores', ''))
        if pd.isna(risk_scores_str) or risk_scores_str == '':
            # Use default low risk values
            for category in risk_categories:
                y_data[category].append(0.1)
            continue
        
        # Parse risk scores
        risk_pairs = risk_scores_str.split(';')
        row_risks = {}
        for pair in risk_pairs:
            if ':' in pair:
                try:
                    cat, score = pair.strip().split(':')
                    cat = cat.strip()
                    score = float(score.strip())
                    row_risks[cat] = score
                except (ValueError, IndexError):
                    continue
        
        # Add risk scores for this row
        for category in risk_categories:
            y_data[category].append(row_risks.get(category, 0.1))
    
    # Create target matrix
    y = np.column_stack([y_data[cat] for cat in risk_categories])
    
    print(f"Target matrix shape: {y.shape}")
    print(f"Feature matrix shape: {X.shape}")
    
    # Train a simple Random Forest model
    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )
    
    print("Training model...")
    model.fit(X, y)
    
    # Evaluate model
    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"Model trained successfully!")
    print(f"MSE: {mse:.4f}")
    print(f"R²: {r2:.4f}")
    
    # Save the model
    model_path = 'health_risk_model.pkl'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    return model

class SimpleHealthModel:
    """Simple health model wrapper"""
    def __init__(self, model, feature_columns):
        self.model = model
        self.feature_columns = feature_columns
        self.n_outputs_ = 10  # Number of risk categories
    
    def predict(self, X):
        return self.model.predict(X)

def main():
    """Main function"""
    print("Starting simplified model training...")
    
    model = create_simple_model()
    if model:
        print("✅ Model training completed successfully!")
        return model
    else:
        print("❌ Model training failed!")
        return None

if __name__ == "__main__":
    main()

