// Results Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Retrieve stored meal data
    const storedData = localStorage.getItem('mealData');
    let mealData = null;
    
    try {
        mealData = storedData ? JSON.parse(storedData) : null;
    } catch (error) {
        console.error('Error parsing stored meal data:', error);
        mealData = null;
    }
    
    if (mealData && typeof mealData === 'object') {
        // Display user data first
        displayUserData(mealData);
        
        // Check if ML analysis is available
        if (mealData.ml_analysis) {
            // Use ML analysis results
            displayMLResults(mealData);
        } else {
            // Fallback to basic analysis
            displayBasicResults(mealData);
        }
    } else {
        // Redirect to input page if no data is available
        window.location.href = 'input.html';
    }
    
    // Save report functionality
    document.getElementById('save-report').addEventListener('click', function() {
        // In a real app, this would generate a PDF or save to user account
        alert('Report saved! In a full implementation, this would generate a PDF report.');
    });
    
    // Mobile navigation
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
    
    // Simple health score calculation (demo purpose)
    function calculateHealthScore(data) {
        let score = 75; // Base score
        
        // Adjust based on meal type
        if (data['meal-type'] === 'breakfast') score += 5;
        if (data['meal-type'] === 'snack') score -= 5;
        
        // Adjust based on portion size
        if (data['portion-size'] === 'small') score += 10;
        if (data['portion-size'] === 'large') score -= 10;
        
        // Adjust based on drink
        if (data.drink === 'water') score += 5;
        if (data.drink === 'soft-drink') score -= 10;
        
        // Ensure score is within 0-100 range
        return Math.max(0, Math.min(100, score));
    }
    
    // Generate key insight based on score and data
    function getKeyInsight(score, data) {
        if (score >= 80) {
            return "Excellent meal choice! You're on the right track for maintaining good health.";
        } else if (score >= 60) {
            return "Good meal overall. Consider adding more vegetables for even better nutrition.";
        } else {
            return "This meal could be improved. Try incorporating more whole foods and reducing processed items.";
        }
    }
    
    // Display user-entered data
    function displayUserData(mealData) {
        // Meal Information
        document.getElementById('user-meal-type').textContent = mealData['meal-type'] || 'Not specified';
        document.getElementById('user-food-items').textContent = mealData['food-items'] || 'Not specified';
        document.getElementById('user-portion-size').textContent = mealData['portion-size'] || 'Not specified';
        document.getElementById('user-drink').textContent = mealData.drink || 'Not specified';
        
        // Personal Information
        document.getElementById('user-age').textContent = mealData.age ? `${mealData.age} years` : 'Not specified';
        document.getElementById('user-gender').textContent = mealData.gender || 'Not specified';
        document.getElementById('user-height').textContent = mealData.height ? `${mealData.height} cm` : 'Not specified';
        document.getElementById('user-weight').textContent = mealData.weight ? `${mealData.weight} kg` : 'Not specified';
        document.getElementById('user-activity-level').textContent = mealData['activity-level'] || 'Not specified';
        
        // Health & Lifestyle
        const conditions = mealData.conditions && mealData.conditions.length > 0 
            ? mealData.conditions.join(', ') 
            : 'None';
        document.getElementById('user-conditions').textContent = conditions;
        
        document.getElementById('user-sleep').textContent = mealData.sleep ? `${mealData.sleep} hours` : 'Not specified';
        document.getElementById('user-water-intake').textContent = mealData['water-intake'] || 'Not specified';
        document.getElementById('user-caffeine').textContent = mealData.caffeine || 'Not specified';
        document.getElementById('user-fruit-veg').textContent = mealData['fruit-veg'] || 'Not specified';
    }
    
    // Display ML analysis results
    function displayMLResults(mealData) {
        const mlAnalysis = mealData.ml_analysis;
        
        // Update meal summary
        document.getElementById('meal-summary').textContent = mealData['food-items'] || 'Meal information not available';
        
        // Update health score
        document.getElementById('health-score').textContent = mlAnalysis.health_score || 75;
        
        // Update key insight
        document.getElementById('key-insight').textContent = mlAnalysis.key_insights || "AI-powered analysis completed.";
        
        // Update risk analysis table with ML predictions
        updateRiskTable(mlAnalysis.risk_predictions);
        
        // Update recommendations
        updateRecommendations(mlAnalysis.recommendations);
        
        // Display food analysis
        displayFoodAnalysis(mlAnalysis.food_analysis);
    }
    
    // Display basic analysis results (fallback)
    function displayBasicResults(mealData) {
        // Populate the results with the meal data
        document.getElementById('meal-summary').textContent = mealData['food-items'] || 'Meal information not available';
        
        // Calculate a simple health score based on meal type and portion size
        const healthScore = calculateHealthScore(mealData);
        document.getElementById('health-score').textContent = healthScore;
        
        // Set key insight based on score
        document.getElementById('key-insight').textContent = getKeyInsight(healthScore, mealData);
    }
    
    // Update risk analysis table
    function updateRiskTable(riskPredictions) {
        const riskTable = document.querySelector('.risk-table tbody');
        if (!riskTable || !riskPredictions) return;
        
        // Clear existing rows
        riskTable.innerHTML = '';
        
        // Add rows for each risk
        const riskCategories = [
            'Type-2-Diabetes', 'Hypertension', 'Cardiovascular-Disease',
            'Obesity-related-illnesses', 'Chronic-Kidney-Disease',
            'Non-alcoholic-Fatty-Liver-Disease', 'Dyslipidemia-related-risk',
            'Gastrointestinal-disorders', 'Osteoporosis', 'Anemia'
        ];
        
        riskCategories.forEach(risk => {
            if (riskPredictions[risk] !== undefined) {
                const row = document.createElement('tr');
                const riskLevel = riskPredictions[risk] > 0.3 ? 'High' : riskPredictions[risk] > 0.1 ? 'Medium' : 'Low';
                const riskPercentage = Math.round(riskPredictions[risk] * 100);
                
                row.innerHTML = `
                    <td>${risk}</td>
                    <td>${riskLevel} (${riskPercentage}%)</td>
                    <td>${getHealthyRange(risk)}</td>
                    <td>${getPrecautions(risk, riskPredictions[risk])}</td>
                `;
                riskTable.appendChild(row);
            }
        });
    }
    
    // Update recommendations section
    function updateRecommendations(recommendations) {
        const recommendationsGrid = document.querySelector('.recommendations-grid');
        if (!recommendationsGrid || !recommendations) return;
        
        // Clear existing recommendations
        recommendationsGrid.innerHTML = '';
        
        // Add new recommendations
        recommendations.forEach((rec, index) => {
            const card = document.createElement('div');
            card.className = 'recommendation-card';
            card.innerHTML = `
                <div class="rec-icon">💡</div>
                <h3>Recommendation ${index + 1}</h3>
                <p>${rec}</p>
            `;
            recommendationsGrid.appendChild(card);
        });
    }
    
    // Display food analysis
    function displayFoodAnalysis(foodAnalysis) {
        if (!foodAnalysis) return;
        
        // You can add a food analysis section to display nutritional breakdown
        console.log('Food Analysis:', foodAnalysis);
    }
    
    // Helper functions
    function getHealthyRange(risk) {
        const ranges = {
            'Type-2-Diabetes': 'Fasting glucose < 100 mg/dL',
            'Hypertension': 'BP < 120/80 mmHg',
            'Cardiovascular-Disease': 'Regular exercise, healthy diet',
            'Obesity-related-illnesses': 'BMI 18.5-24.9',
            'Chronic-Kidney-Disease': 'Regular checkups, control BP',
            'Non-alcoholic-Fatty-Liver-Disease': 'Limit alcohol, maintain weight',
            'Dyslipidemia-related-risk': 'Total cholesterol < 200 mg/dL',
            'Gastrointestinal-disorders': 'High fiber, regular meals',
            'Osteoporosis': 'Calcium, Vitamin D, weight-bearing exercise',
            'Anemia': 'Iron-rich foods, B12 sources'
        };
        return ranges[risk] || 'Consult healthcare provider';
    }
    
    function getPrecautions(risk, score) {
        if (score > 0.3) {
            return 'High risk - Consult healthcare provider immediately';
        } else if (score > 0.1) {
            return 'Moderate risk - Monitor and take preventive measures';
        } else {
            return 'Low risk - Maintain current healthy lifestyle';
        }
    }
});