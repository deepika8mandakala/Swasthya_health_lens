// Input System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const mealForm = document.getElementById('meal-form');
    const foodItemsTextarea = document.getElementById('food-items');
    const suggestionTags = document.querySelectorAll('.suggestion-tag');
    
    // Add click event to suggestion tags
    suggestionTags.forEach(tag => {
        tag.addEventListener('click', function() {
            const currentText = foodItemsTextarea.value;
            const suggestionText = this.textContent;
            
            if (currentText) {
                foodItemsTextarea.value = currentText + ', ' + suggestionText;
            } else {
                foodItemsTextarea.value = suggestionText;
            }
            
            // Focus on the textarea
            foodItemsTextarea.focus();
        });
    });
    
    // Form submission
    mealForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Basic validation
        if (!validateForm()) {
            return;
        }
        
        // Show loading state
        const submitButton = this.querySelector('button[type="submit"]');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Analyzing...';
        submitButton.disabled = true;
        
        // Collect form data
        const formData = new FormData(mealForm);
        const data = Object.fromEntries(formData);
        
        // Get selected conditions
        const conditions = [];
        document.querySelectorAll('input[name="conditions"]:checked').forEach(checkbox => {
            conditions.push(checkbox.value);
        });
        data.conditions = conditions;
        
        // Call ML API
        analyzeMealWithML(data, submitButton, originalText);
    });
    
    // Form validation
    function validateForm() {
        const requiredFields = mealForm.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                highlightError(field);
            } else {
                removeErrorHighlight(field);
            }
        });
        
        // Validate age range
        const ageField = document.getElementById('age');
        if (ageField.value && ageField.value.trim() !== '') {
            const age = parseInt(ageField.value);
            if (isNaN(age) || age < 1 || age > 120) {
                isValid = false;
                highlightError(ageField, 'Please enter a valid age (1-120)');
            }
        }
        
        // Validate height and weight ranges
        const heightField = document.getElementById('height');
        if (heightField.value && heightField.value.trim() !== '') {
            const height = parseInt(heightField.value);
            if (isNaN(height) || height < 50 || height > 250) {
                isValid = false;
                highlightError(heightField, 'Please enter a valid height (50-250 cm)');
            }
        }
        
        const weightField = document.getElementById('weight');
        if (weightField.value && weightField.value.trim() !== '') {
            const weight = parseInt(weightField.value);
            if (isNaN(weight) || weight < 5 || weight > 300) {
                isValid = false;
                highlightError(weightField, 'Please enter a valid weight (5-300 kg)');
            }
        }
        
        return isValid;
    }
    
    function highlightError(field, message = 'This field is required') {
        field.classList.add('error');
        
        // Remove existing error message
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = message;
        
        field.parentNode.appendChild(errorMessage);
    }
    
    function removeErrorHighlight(field) {
        field.classList.remove('error');
        
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
    }
    
    // Real-time validation for required fields
    const requiredFields = mealForm.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.value.trim()) {
                highlightError(this);
            } else {
                removeErrorHighlight(this);
            }
        });
    });
    
    // Real-time validation for numeric fields
    const numericFields = ['age', 'height', 'weight'];
    numericFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('blur', function() {
                if (this.value.trim() !== '') {
                    const value = parseInt(this.value);
                    let isValid = true;
                    let errorMessage = '';
                    
                    if (fieldId === 'age' && (isNaN(value) || value < 1 || value > 120)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid age (1-120)';
                    } else if (fieldId === 'height' && (isNaN(value) || value < 50 || value > 250)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid height (50-250 cm)';
                    } else if (fieldId === 'weight' && (isNaN(value) || value < 5 || value > 300)) {
                        isValid = false;
                        errorMessage = 'Please enter a valid weight (5-300 kg)';
                    }
                    
                    if (isValid) {
                        removeErrorHighlight(this);
                    } else {
                        highlightError(this, errorMessage);
                    }
                }
            });
        }
    });
    
    // Mobile navigation (same as main.js)
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }));
    }
});

// ML API Integration
async function analyzeMealWithML(data, submitButton, originalText) {
    try {
        // Prepare data for ML API
        const mlData = {
            'food-items': data['food-items'],
            'meal-type': data['meal-type'],
            'portion-size': data['portion-size'],
            'drink': data.drink,
            'age': parseInt(data.age),
            'gender': data.gender,
            'height': parseInt(data.height),
            'weight': parseInt(data.weight),
            'activity-level': data['activity-level'],
            'diet-pattern': 'vegetarian', // Default, could be enhanced
            'snack-freq': 'rare', // Default, could be enhanced
            'smoking-status': 'never', // Default, could be enhanced
            'meals-per-day': 3, // Default
            'water-intake': data['water-intake'] || '2-3l',
            'sleep': parseFloat(data.sleep) || 7,
            'alcohol': 0, // Default
            'conditions': data.conditions
        };
        
        // Call ML API
        const response = await fetch('http://localhost:5000/api/analyze-meal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(mlData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Store enhanced data for results page
        const enhancedData = {
            ...data,
            ml_analysis: result
        };
        
        localStorage.setItem('mealData', JSON.stringify(enhancedData));
        
        // Redirect to results page
        window.location.href = 'results.html';
        
    } catch (error) {
        console.error('Error calling ML API:', error);
        
        // Fallback to basic analysis
        const basicData = {
            ...data,
            ml_analysis: {
                health_score: calculateBasicHealthScore(data),
                food_analysis: {
                    food_items: data['food-items'].split(',').map(item => item.trim()),
                    nutrition: { carbs: 0.3, protein: 0.1, fat: 0.05, fiber: 0.05 }
                },
                risk_predictions: getDefaultRisks(),
                recommendations: getBasicRecommendations(data),
                key_insights: "Basic analysis completed. For detailed insights, ensure the ML server is running."
            }
        };
        
        localStorage.setItem('mealData', JSON.stringify(basicData));
        window.location.href = 'results.html';
    } finally {
        // Reset button
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
}

function calculateBasicHealthScore(data) {
    let score = 50;
    
    // Adjust based on meal type
    if (data['meal-type'] === 'breakfast') score += 10;
    if (data['meal-type'] === 'snack') score -= 10;
    
    // Adjust based on portion size
    if (data['portion-size'] === 'small') score += 10;
    if (data['portion-size'] === 'large') score -= 10;
    
    // Adjust based on drink
    if (data.drink === 'water') score += 10;
    if (data.drink === 'soft-drink') score -= 15;
    
    return Math.max(0, Math.min(100, score));
}

function getDefaultRisks() {
    return {
        'Type-2-Diabetes': 0.1,
        'Hypertension': 0.1,
        'Cardiovascular-Disease': 0.1,
        'Obesity-related-illnesses': 0.1,
        'Chronic-Kidney-Disease': 0.05,
        'Non-alcoholic-Fatty-Liver-Disease': 0.05,
        'Dyslipidemia-related-risk': 0.1,
        'Gastrointestinal-disorders': 0.05,
        'Osteoporosis': 0.05,
        'Anemia': 0.05
    };
}

function getBasicRecommendations(data) {
    const recommendations = [];
    
    if (data['portion-size'] === 'large') {
        recommendations.push("Consider reducing portion size for better health.");
    }
    
    if (data.drink === 'soft-drink') {
        recommendations.push("Try replacing soft drinks with water or herbal tea.");
    }
    
    if (data['activity-level'] === 'sedentary') {
        recommendations.push("Increase physical activity for better health.");
    }
    
    if (data.sleep < 6) {
        recommendations.push("Aim for 7-8 hours of sleep per night.");
    }
    
    return recommendations;
}