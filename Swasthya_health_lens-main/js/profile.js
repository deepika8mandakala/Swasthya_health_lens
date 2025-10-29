// Profile Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profile-form');
    const loadProfileBtn = document.getElementById('load-profile');
    
    // Load saved profile on page load
    loadSavedProfile();
    
    // Form submission
    profileForm.addEventListener('submit', function(e) {
        e.preventDefault();
        saveProfile();
    });
    
    // Load profile button
    loadProfileBtn.addEventListener('click', function() {
        loadSavedProfile();
    });
    
    // Real-time BMI calculation
    const heightField = document.getElementById('profile-height');
    const weightField = document.getElementById('profile-weight');
    
    [heightField, weightField].forEach(field => {
        field.addEventListener('input', calculateBMI);
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
    
    function saveProfile() {
        const formData = new FormData(profileForm);
        const profileData = Object.fromEntries(formData);
        
        // Get selected conditions
        const conditions = [];
        document.querySelectorAll('input[name="conditions"]:checked').forEach(checkbox => {
            conditions.push(checkbox.value);
        });
        profileData.conditions = conditions;
        
        // Get selected goals
        const goals = [];
        document.querySelectorAll('input[name="goals"]:checked').forEach(checkbox => {
            goals.push(checkbox.value);
        });
        profileData.goals = goals;
        
        // Calculate BMI
        const height = parseFloat(profileData.height);
        const weight = parseFloat(profileData.weight);
        if (height && weight) {
            profileData.bmi = calculateBMIValue(height, weight);
        }
        
        // Save to localStorage
        localStorage.setItem('userProfile', JSON.stringify(profileData));
        
        // Update stats
        updateProfileStats(profileData);
        
        // Show success message
        showNotification('Profile saved successfully!', 'success');
        
        console.log('Profile saved:', profileData);
    }
    
    function loadSavedProfile() {
        const savedProfile = localStorage.getItem('userProfile');
        if (savedProfile) {
            try {
                const profileData = JSON.parse(savedProfile);
                
                // Fill form fields
                Object.keys(profileData).forEach(key => {
                    const field = document.getElementById(`profile-${key}`);
                    if (field) {
                        if (field.type === 'checkbox') {
                            field.checked = profileData[key].includes(field.value);
                        } else {
                            field.value = profileData[key];
                        }
                    }
                });
                
                // Handle conditions checkboxes
                if (profileData.conditions) {
                    document.querySelectorAll('input[name="conditions"]').forEach(checkbox => {
                        checkbox.checked = profileData.conditions.includes(checkbox.value);
                    });
                }
                
                // Handle goals checkboxes
                if (profileData.goals) {
                    document.querySelectorAll('input[name="goals"]').forEach(checkbox => {
                        checkbox.checked = profileData.goals.includes(checkbox.value);
                    });
                }
                
                // Update stats
                updateProfileStats(profileData);
                
                showNotification('Profile loaded successfully!', 'success');
                
            } catch (error) {
                console.error('Error loading profile:', error);
                showNotification('Error loading profile', 'error');
            }
        } else {
            showNotification('No saved profile found', 'info');
        }
    }
    
    function calculateBMI() {
        const height = parseFloat(heightField.value);
        const weight = parseFloat(weightField.value);
        
        if (height && weight) {
            const bmi = calculateBMIValue(height, weight);
            document.getElementById('bmi-value').textContent = bmi.toFixed(1);
            
            // Update BMI category
            const bmiCategory = getBMICategory(bmi);
            const bmiElement = document.getElementById('bmi-value');
            bmiElement.className = `bmi-${bmiCategory.toLowerCase().replace(' ', '-')}`;
        }
    }
    
    function calculateBMIValue(height, weight) {
        const heightM = height / 100;
        return weight / (heightM * heightM);
    }
    
    function getBMICategory(bmi) {
        if (bmi < 18.5) return 'Underweight';
        if (bmi < 25) return 'Normal';
        if (bmi < 30) return 'Overweight';
        return 'Obese';
    }
    
    function updateProfileStats(profileData) {
        // Update BMI
        if (profileData.bmi) {
            document.getElementById('bmi-value').textContent = profileData.bmi.toFixed(1);
        }
        
        // Update health score (simplified calculation)
        const healthScore = calculateHealthScore(profileData);
        document.getElementById('health-score-value').textContent = healthScore;
        
        // Update meals analyzed (from localStorage)
        const mealsAnalyzed = getMealsAnalyzedCount();
        document.getElementById('meals-analyzed').textContent = mealsAnalyzed;
        
        // Update streak (simplified)
        const streak = getAnalysisStreak();
        document.getElementById('analysis-streak').textContent = streak;
    }
    
    function calculateHealthScore(profileData) {
        let score = 50; // Base score
        
        // Age factor
        const age = parseInt(profileData.age) || 30;
        if (age >= 18 && age <= 65) score += 10;
        else if (age > 65) score += 5;
        
        // BMI factor
        const bmi = parseFloat(profileData.bmi) || 22;
        if (bmi >= 18.5 && bmi < 25) score += 15;
        else if (bmi >= 25 && bmi < 30) score += 5;
        else if (bmi < 18.5 || bmi >= 30) score -= 10;
        
        // Activity level factor
        const activity = profileData['activity-level'] || 'moderate';
        const activityScores = {
            'sedentary': -10,
            'light': 0,
            'moderate': 10,
            'active': 15,
            'very-active': 20
        };
        score += activityScores[activity] || 0;
        
        // Sleep factor
        const sleep = parseFloat(profileData.sleep) || 7;
        if (sleep >= 7 && sleep <= 9) score += 10;
        else if (sleep >= 6 && sleep < 7) score += 5;
        else if (sleep < 6) score -= 10;
        
        // Water intake factor
        const water = profileData['water-intake'] || '2-3l';
        if (water === '2-3l' || water === 'more-than-3l') score += 5;
        else if (water === '1-2l') score += 0;
        else score -= 5;
        
        // Conditions factor
        const conditions = profileData.conditions || [];
        if (conditions.includes('none') || conditions.length === 0) score += 10;
        else score -= conditions.length * 5;
        
        return Math.max(0, Math.min(100, score));
    }
    
    function getMealsAnalyzedCount() {
        // Count stored meal analyses
        let count = 0;
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith('meal_analysis_')) {
                count++;
            }
        }
        return count;
    }
    
    function getAnalysisStreak() {
        // Simple streak calculation based on recent analyses
        const today = new Date().toDateString();
        const yesterday = new Date(Date.now() - 86400000).toDateString();
        
        let streak = 0;
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith('meal_analysis_')) {
                const data = JSON.parse(localStorage.getItem(key));
                const analysisDate = new Date(data.timestamp).toDateString();
                if (analysisDate === today || analysisDate === yesterday) {
                    streak++;
                }
            }
        }
        return streak;
    }
    
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        // Set background color based on type
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            info: '#3b82f6',
            warning: '#f59e0b'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    // Auto-save profile every 30 seconds
    setInterval(() => {
        const formData = new FormData(profileForm);
        const profileData = Object.fromEntries(formData);
        
        if (profileData.name && profileData.age) {
            // Only auto-save if there's meaningful data
            const conditions = [];
            document.querySelectorAll('input[name="conditions"]:checked').forEach(checkbox => {
                conditions.push(checkbox.value);
            });
            profileData.conditions = conditions;
            
            const goals = [];
            document.querySelectorAll('input[name="goals"]:checked').forEach(checkbox => {
                goals.push(checkbox.value);
            });
            profileData.goals = goals;
            
            localStorage.setItem('userProfile', JSON.stringify(profileData));
        }
    }, 30000);
});

