"""
Health Risk Prediction Model Training
Trains Random Forest models for predicting various health risks
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

class HealthRiskPredictor:
    def __init__(self, dataset_path: str = '../health_dataset_india_2000.csv'):
        """Initialize the health risk predictor"""
        self.dataset_path = dataset_path
        self.models = {}
        self.encoders = {}
        self.feature_columns = [
            'age', 'gender_encoded', 'height_cm', 'weight_kg', 'bmi', 'waist_cm',
            'activity_level_encoded', 'diet_pattern_encoded', 'meals_per_day',
            'snack_freq_encoded', 'water_l_per_day', 'sleep_h', 'smoking_status_encoded',
            'alcohol_units_week', 'family_history_diabetes', 'family_history_heart',
            'bp_sys', 'bp_dia', 'fasting_glucose_mg_dl', 'cholesterol_total_mg_dl'
        ]
        
        self.risk_categories = [
            'Type-2-Diabetes', 'Hypertension', 'Cardiovascular-Disease',
            'Obesity-related-illnesses', 'Chronic-Kidney-Disease',
            'Non-alcoholic-Fatty-Liver-Disease', 'Dyslipidemia-related-risk',
            'Gastrointestinal-disorders', 'Osteoporosis', 'Anemia',
            'Certain-Cancers (diet-related)', 'Metabolic-Syndrome',
            'Depression-Anxiety', 'PCOS (female-specific)', 'COPD (smoking)',
            'Liver-cirrhosis', 'Stroke', 'Gallstones', 'Hypothyroidism',
            'Oral-health-issues'
        ]
    
    def load_and_preprocess_data(self) -> pd.DataFrame:
        """Load and preprocess the health dataset"""
        print("Loading dataset...")
        
        # Load the dataset
        df = pd.read_csv(self.dataset_path)
        print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Create a copy for preprocessing
        df_processed = df.copy()
        
        # Encode categorical variables
        print("Encoding categorical variables...")
        
        # Gender encoding
        gender_mapping = {'Male': 1, 'Female': 0, 'male': 1, 'female': 0}
        df_processed['gender_encoded'] = df_processed['gender'].map(gender_mapping)
        
        # Activity level encoding
        activity_mapping = {
            'Sedentary': 0, 'Light': 1, 'Moderate': 2, 'Active': 3, 'Very Active': 4,
            'sedentary': 0, 'light': 1, 'moderate': 2, 'active': 3, 'very-active': 4
        }
        df_processed['activity_level_encoded'] = df_processed['activity_level'].map(activity_mapping)
        
        # Diet pattern encoding
        diet_mapping = {
            'Vegetarian': 0, 'Non-vegetarian': 1, 'Eggetarian': 0.5,
            'Lacto-vegetarian': 0.3, 'North-Indian': 0.7,
            'vegetarian': 0, 'non-vegetarian': 1, 'eggetarian': 0.5,
            'lacto-vegetarian': 0.3, 'north-indian': 0.7
        }
        df_processed['diet_pattern_encoded'] = df_processed['diet_pattern'].map(diet_mapping)
        
        # Snack frequency encoding
        snack_mapping = {
            'Never': 0, 'Rare': 1, 'Weekly': 2, 'Daily': 3,
            'never': 0, 'rare': 1, 'weekly': 2, 'daily': 3
        }
        df_processed['snack_freq_encoded'] = df_processed['snack_freq'].map(snack_mapping)
        
        # Smoking status encoding
        smoking_mapping = {
            'Never': 0, 'Former': 1, 'Current': 2,
            'never': 0, 'former': 1, 'current': 2
        }
        df_processed['smoking_status_encoded'] = df_processed['smoking_status'].map(smoking_mapping)
        
        # Handle missing values
        print("Handling missing values...")
        
        # Fill missing categorical values with default values
        df_processed['gender_encoded'] = df_processed['gender_encoded'].fillna(1)  # Default to male
        df_processed['activity_level_encoded'] = df_processed['activity_level_encoded'].fillna(2)  # Default to moderate
        df_processed['diet_pattern_encoded'] = df_processed['diet_pattern_encoded'].fillna(0)  # Default to vegetarian
        df_processed['snack_freq_encoded'] = df_processed['snack_freq_encoded'].fillna(1)  # Default to rare
        df_processed['smoking_status_encoded'] = df_processed['smoking_status_encoded'].fillna(0)  # Default to never
        
        # Fill other missing values with median
        df_processed = df_processed.fillna(df_processed.median())
        
        # Ensure all required columns exist
        for col in self.feature_columns:
            if col not in df_processed.columns:
                print(f"Warning: Column {col} not found, creating with default values")
                if 'encoded' in col:
                    df_processed[col] = 0
                else:
                    df_processed[col] = df_processed[col.split('_')[0]] if col.split('_')[0] in df_processed.columns else 0
        
        print("Data preprocessing completed")
        return df_processed
    
    def parse_risk_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Parse risk scores from the risk_scores column"""
        print("Parsing risk scores...")
        
        # Initialize risk score columns
        for category in self.risk_categories:
            df[f'risk_{category}'] = 0.0
        
        # Parse risk scores from the risk_scores column
        for idx, row in df.iterrows():
            risk_scores_str = str(row.get('risk_scores', ''))
            if pd.isna(risk_scores_str) or risk_scores_str == '':
                continue
            
            # Split by semicolon and parse each risk
            risk_pairs = risk_scores_str.split(';')
            for pair in risk_pairs:
                if ':' in pair:
                    try:
                        category, score = pair.strip().split(':')
                        category = category.strip()
                        score = float(score.strip())
                        
                        if category in self.risk_categories:
                            df.at[idx, f'risk_{category}'] = score
                    except (ValueError, IndexError):
                        continue
        
        print("Risk scores parsed successfully")
        return df
    
    def train_models(self, df: pd.DataFrame) -> Dict:
        """Train Random Forest models for each risk category"""
        print("Training models...")
        
        # Prepare features
        X = df[self.feature_columns].values
        
        # Train a model for each risk category
        for category in self.risk_categories:
            print(f"Training model for {category}...")
            
            # Get target variable
            target_col = f'risk_{category}'
            if target_col not in df.columns:
                print(f"Warning: Target column {target_col} not found, skipping")
                continue
            
            y = df[target_col].values
            
            # Remove rows with missing target values
            valid_indices = ~np.isnan(y)
            X_valid = X[valid_indices]
            y_valid = y[valid_indices]
            
            if len(X_valid) == 0:
                print(f"Warning: No valid data for {category}, skipping")
                continue
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_valid, y_valid, test_size=0.2, random_state=42
            )
            
            # Train Random Forest model
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            print(f"  {category}: MSE={mse:.4f}, R²={r2:.4f}")
            
            # Store model
            self.models[category] = model
        
        print(f"Training completed. {len(self.models)} models trained.")
        return self.models
    
    def create_ensemble_model(self) -> object:
        """Create an ensemble model that can predict all risk categories"""
        print("Creating ensemble model...")
        
        # This is a simplified approach - in practice, you might want separate models
        # or a multi-output model depending on your specific needs
        
        class EnsembleHealthModel:
            def __init__(self, individual_models, feature_columns):
                self.individual_models = individual_models
                self.feature_columns = feature_columns
                self.n_outputs_ = len(individual_models)
            
            def predict(self, X):
                predictions = []
                for category in self.individual_models.keys():
                    pred = self.individual_models[category].predict(X)
                    predictions.append(pred)
                return np.column_stack(predictions)
        
        ensemble = EnsembleHealthModel(self.models, self.feature_columns)
        return ensemble
    
    def train_model(self) -> object:
        """Main training function"""
        print("Starting health risk prediction model training...")
        
        # Load and preprocess data
        df = self.load_and_preprocess_data()
        
        # Parse risk scores
        df = self.parse_risk_scores(df)
        
        # Train individual models
        self.train_models(df)
        
        # Create ensemble model
        ensemble_model = self.create_ensemble_model()
        
        # Save the ensemble model
        model_path = 'health_risk_model.pkl'
        joblib.dump(ensemble_model, model_path)
        print(f"Model saved to {model_path}")
        
        # Save individual models for reference
        for category, model in self.models.items():
            model_path = f'model_{category.replace(" ", "_").replace("(", "").replace(")", "").lower()}.pkl'
            joblib.dump(model, model_path)
        
        print("Training completed successfully!")
        return ensemble_model
    
    def evaluate_model(self, model, X_test, y_test) -> Dict:
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        
        metrics = {
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        return metrics

def main():
    """Main function to train the model"""
    # Check if dataset exists
    dataset_path = '../health_dataset_india_2000.csv'
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset not found at {dataset_path}")
        print("Please ensure the dataset file is in the parent directory")
        return None
    
    # Initialize and train the model
    predictor = HealthRiskPredictor(dataset_path)
    model = predictor.train_model()
    
    return model

if __name__ == "__main__":
    model = main()
    if model:
        print("Model training completed successfully!")
    else:
        print("Model training failed!")

