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
        
        // Simulate API call/processing
        setTimeout(() => {
            // Collect form data
            const formData = new FormData(mealForm);
            const data = Object.fromEntries(formData);
            
            // Store data for results page
            localStorage.setItem('mealData', JSON.stringify(data));
            
            // Redirect to results page
            window.location.href = 'results.html';
        }, 1500);
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
        if (ageField.value) {
            const age = parseInt(ageField.value);
            if (age < 1 || age > 120) {
                isValid = false;
                highlightError(ageField, 'Please enter a valid age (1-120)');
            }
        }
        
        return isValid;
    }
    
    function highlightError(field, message = 'This field is required') {
        field.style.borderColor = '#ef4444';
        field.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
        
        // Remove existing error message
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Add error message
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.style.color = '#ef4444';
        errorMessage.style.fontSize = '0.8rem';
        errorMessage.style.marginTop = '5px';
        errorMessage.textContent = message;
        
        field.parentNode.appendChild(errorMessage);
    }
    
    function removeErrorHighlight(field) {
        field.style.borderColor = '#d1d5db';
        field.style.boxShadow = 'none';
        
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