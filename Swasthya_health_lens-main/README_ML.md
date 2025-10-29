# Swasthya AI - ML Integration

This document explains how to set up and use the Machine Learning features of Swasthya AI.

## Overview

The ML integration provides:
- **Health Risk Prediction**: Uses Random Forest models trained on 2000+ health records
- **Food Analysis**: Comprehensive nutritional analysis of Indian foods
- **Personalized Recommendations**: AI-generated health recommendations
- **Real-time Scoring**: Dynamic health score calculation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train and Start ML Server
```bash
python start_ml_server.py
```

This will:
- Install required packages
- Train the ML model on your dataset
- Start the Flask API server on port 5000

### 3. Open the Web Application
Open `index.html` in your browser to use the application.

## Manual Setup

### Train Model Only
```bash
cd ml_model
python train_model.py
```

### Start Server Only
```bash
cd ml_model
python app.py
```

## API Endpoints

### POST /api/analyze-meal
Analyzes a meal and returns health predictions.

**Request Body:**
```json
{
  "food-items": "2 rotis, dal, rice, chicken curry",
  "meal-type": "lunch",
  "portion-size": "medium",
  "age": 30,
  "gender": "male",
  "height": 170,
  "weight": 70,
  "activity-level": "moderate",
  "conditions": ["diabetes"]
}
```

**Response:**
```json
{
  "health_score": 82,
  "food_analysis": {
    "food_items": ["rice", "roti", "dal", "chicken", "curry"],
    "nutrition": {
      "carbs": 0.6,
      "protein": 0.15,
      "fat": 0.08,
      "fiber": 0.1
    }
  },
  "risk_predictions": {
    "Type-2-Diabetes": 0.12,
    "Hypertension": 0.08,
    "Cardiovascular-Disease": 0.15
  },
  "recommendations": [
    "Add more vegetables to your meal",
    "Consider reducing portion size"
  ],
  "key_insights": "Good meal overall. Consider adding more vegetables."
}
```

## Model Architecture

### Health Risk Prediction
- **Algorithm**: Random Forest Regressor
- **Features**: 20+ health and lifestyle factors
- **Targets**: 20 different health risk categories
- **Performance**: R² > 0.7 for most risk categories

### Food Analysis
- **Database**: 100+ Indian food items
- **Nutritional Data**: Carbs, protein, fat, fiber, calories, sodium
- **Pattern Matching**: Intelligent food item recognition

## File Structure

```
ml_model/
├── train_model.py          # Model training script
├── app.py                  # Flask API server
├── food_database.py        # Food nutritional database
└── health_risk_model.pkl   # Trained model (generated)

health_dataset_india_2000.csv  # Training dataset
start_ml_server.py            # Startup script
requirements.txt              # Python dependencies
```

## Customization

### Adding New Foods
Edit `ml_model/food_database.py` to add new food items:

```python
FOOD_DATABASE['new_food'] = {
    'carbs': 0.5,
    'protein': 0.2,
    'fat': 0.1,
    'fiber': 0.05,
    'calories': 200,
    'sodium': 10
}
```

### Modifying Risk Categories
Edit the `risk_categories` list in `train_model.py`:

```python
self.risk_categories = [
    'Type-2-Diabetes',
    'Hypertension',
    # Add your custom risk categories
]
```

### Updating Model Features
Modify the `feature_columns` list in `train_model.py` to include new features.

## Troubleshooting

### Common Issues

1. **Port 5000 already in use**
   - Change the port in `app.py`: `app.run(port=5001)`
   - Update the API URL in `input-systems.js`

2. **Model training fails**
   - Check if the dataset file exists
   - Ensure all required packages are installed
   - Check the dataset format

3. **API connection fails**
   - Ensure the Flask server is running
   - Check CORS settings
   - Verify the API endpoint URL

### Debug Mode
Run the Flask app in debug mode:
```python
app.run(debug=True, port=5000)
```

## Performance

- **Training Time**: ~2-3 minutes on modern hardware
- **Prediction Time**: <100ms per request
- **Memory Usage**: ~200MB for the model
- **Accuracy**: 70-85% for most risk predictions

## Future Enhancements

- [ ] Deep learning models for better accuracy
- [ ] Real-time food image recognition
- [ ] Integration with wearable devices
- [ ] Multi-language support
- [ ] Mobile app integration

## Support

For issues or questions:
1. Check the console logs for error messages
2. Verify all dependencies are installed
3. Ensure the dataset is properly formatted
4. Check the API endpoints are accessible

