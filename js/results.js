// Results Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Retrieve stored meal data
    const mealData = JSON.parse(localStorage.getItem('mealData'));
    
    if (mealData) {
        // Populate the results with the meal data
        document.getElementById('meal-summary').textContent = mealData['food-items'] || 'Meal information not available';
        
        // Calculate a simple health score based on meal type and portion size
        const healthScore = calculateHealthScore(mealData);
        document.getElementById('health-score').textContent = healthScore;
        
        // Set key insight based on score
        document.getElementById('key-insight').textContent = getKeyInsight(healthScore, mealData);
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
});