"""
Food Database for Indian Cuisine
Contains nutritional information for common Indian food items
"""

import re
from typing import Dict, List, Tuple

# Comprehensive Indian food database with nutritional values per 100g
FOOD_DATABASE = {
    # Rice and Grains
    'rice': {'carbs': 0.78, 'protein': 0.07, 'fat': 0.01, 'fiber': 0.01, 'calories': 130, 'sodium': 1},
    'basmati rice': {'carbs': 0.78, 'protein': 0.07, 'fat': 0.01, 'fiber': 0.01, 'calories': 130, 'sodium': 1},
    'brown rice': {'carbs': 0.72, 'protein': 0.08, 'fat': 0.03, 'fiber': 0.03, 'calories': 111, 'sodium': 5},
    'jeera rice': {'carbs': 0.78, 'protein': 0.07, 'fat': 0.05, 'fiber': 0.01, 'calories': 140, 'sodium': 2},
    'pulao': {'carbs': 0.75, 'protein': 0.08, 'fat': 0.08, 'fiber': 0.02, 'calories': 150, 'sodium': 3},
    'biryani': {'carbs': 0.70, 'protein': 0.12, 'fat': 0.12, 'fiber': 0.02, 'calories': 180, 'sodium': 5},
    
    # Wheat and Breads
    'roti': {'carbs': 0.45, 'protein': 0.12, 'fat': 0.02, 'fiber': 0.02, 'calories': 120, 'sodium': 2},
    'chapati': {'carbs': 0.45, 'protein': 0.12, 'fat': 0.02, 'fiber': 0.02, 'calories': 120, 'sodium': 2},
    'naan': {'carbs': 0.50, 'protein': 0.10, 'fat': 0.08, 'fiber': 0.01, 'calories': 140, 'sodium': 3},
    'paratha': {'carbs': 0.40, 'protein': 0.10, 'fat': 0.15, 'fiber': 0.02, 'calories': 180, 'sodium': 2},
    'puri': {'carbs': 0.35, 'protein': 0.08, 'fat': 0.25, 'fiber': 0.01, 'calories': 200, 'sodium': 1},
    'bread': {'carbs': 0.50, 'protein': 0.10, 'fat': 0.03, 'fiber': 0.02, 'calories': 120, 'sodium': 4},
    'whole wheat bread': {'carbs': 0.45, 'protein': 0.12, 'fat': 0.04, 'fiber': 0.06, 'calories': 110, 'sodium': 3},
    
    # Lentils and Pulses
    'dal': {'carbs': 0.20, 'protein': 0.25, 'fat': 0.01, 'fiber': 0.08, 'calories': 120, 'sodium': 2},
    'toor dal': {'carbs': 0.20, 'protein': 0.25, 'fat': 0.01, 'fiber': 0.08, 'calories': 120, 'sodium': 2},
    'moong dal': {'carbs': 0.18, 'protein': 0.24, 'fat': 0.01, 'fiber': 0.10, 'calories': 110, 'sodium': 1},
    'chana dal': {'carbs': 0.22, 'protein': 0.20, 'fat': 0.02, 'fiber': 0.12, 'calories': 115, 'sodium': 1},
    'masoor dal': {'carbs': 0.19, 'protein': 0.26, 'fat': 0.01, 'fiber': 0.09, 'calories': 118, 'sodium': 1},
    'rajma': {'carbs': 0.25, 'protein': 0.22, 'fat': 0.01, 'fiber': 0.15, 'calories': 130, 'sodium': 1},
    'chole': {'carbs': 0.25, 'protein': 0.22, 'fat': 0.01, 'fiber': 0.15, 'calories': 130, 'sodium': 1},
    'black gram': {'carbs': 0.20, 'protein': 0.25, 'fat': 0.01, 'fiber': 0.10, 'calories': 120, 'sodium': 1},
    
    # Vegetables
    'potato': {'carbs': 0.17, 'protein': 0.02, 'fat': 0.001, 'fiber': 0.02, 'calories': 77, 'sodium': 6},
    'onion': {'carbs': 0.09, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.02, 'calories': 40, 'sodium': 4},
    'tomato': {'carbs': 0.04, 'protein': 0.01, 'fat': 0.002, 'fiber': 0.01, 'calories': 18, 'sodium': 5},
    'carrot': {'carbs': 0.10, 'protein': 0.01, 'fat': 0.002, 'fiber': 0.03, 'calories': 41, 'sodium': 69},
    'cabbage': {'carbs': 0.06, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.02, 'calories': 25, 'sodium': 18},
    'cauliflower': {'carbs': 0.05, 'protein': 0.02, 'fat': 0.001, 'fiber': 0.02, 'calories': 25, 'sodium': 30},
    'spinach': {'carbs': 0.04, 'protein': 0.03, 'fat': 0.004, 'fiber': 0.02, 'calories': 23, 'sodium': 79},
    'okra': {'carbs': 0.07, 'protein': 0.02, 'fat': 0.001, 'fiber': 0.03, 'calories': 33, 'sodium': 7},
    'brinjal': {'carbs': 0.06, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.03, 'calories': 25, 'sodium': 2},
    'bitter gourd': {'carbs': 0.04, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.02, 'calories': 17, 'sodium': 2},
    'bottle gourd': {'carbs': 0.04, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.01, 'calories': 12, 'sodium': 2},
    'ridge gourd': {'carbs': 0.04, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.01, 'calories': 20, 'sodium': 2},
    'green beans': {'carbs': 0.07, 'protein': 0.02, 'fat': 0.001, 'fiber': 0.03, 'calories': 31, 'sodium': 6},
    'peas': {'carbs': 0.14, 'protein': 0.05, 'fat': 0.001, 'fiber': 0.05, 'calories': 81, 'sodium': 5},
    'corn': {'carbs': 0.19, 'protein': 0.03, 'fat': 0.01, 'fiber': 0.02, 'calories': 86, 'sodium': 1},
    
    # Non-vegetarian
    'chicken': {'carbs': 0.00, 'protein': 0.27, 'fat': 0.14, 'fiber': 0.00, 'calories': 165, 'sodium': 74},
    'chicken curry': {'carbs': 0.05, 'protein': 0.20, 'fat': 0.12, 'fiber': 0.01, 'calories': 180, 'sodium': 200},
    'mutton': {'carbs': 0.00, 'protein': 0.25, 'fat': 0.21, 'fiber': 0.00, 'calories': 250, 'sodium': 72},
    'fish': {'carbs': 0.00, 'protein': 0.22, 'fat': 0.12, 'fiber': 0.00, 'calories': 206, 'sodium': 61},
    'fish curry': {'carbs': 0.05, 'protein': 0.18, 'fat': 0.10, 'fiber': 0.01, 'calories': 160, 'sodium': 180},
    'egg': {'carbs': 0.01, 'protein': 0.13, 'fat': 0.11, 'fiber': 0.00, 'calories': 155, 'sodium': 124},
    'prawns': {'carbs': 0.00, 'protein': 0.24, 'fat': 0.01, 'fiber': 0.00, 'calories': 99, 'sodium': 111},
    
    # Dairy
    'milk': {'carbs': 0.05, 'protein': 0.03, 'fat': 0.03, 'fiber': 0.00, 'calories': 42, 'sodium': 44},
    'curd': {'carbs': 0.04, 'protein': 0.10, 'fat': 0.04, 'fiber': 0.00, 'calories': 59, 'sodium': 36},
    'yogurt': {'carbs': 0.04, 'protein': 0.10, 'fat': 0.04, 'fiber': 0.00, 'calories': 59, 'sodium': 36},
    'paneer': {'carbs': 0.02, 'protein': 0.18, 'fat': 0.20, 'fiber': 0.00, 'calories': 265, 'sodium': 15},
    'cheese': {'carbs': 0.01, 'protein': 0.25, 'fat': 0.33, 'fiber': 0.00, 'calories': 356, 'sodium': 621},
    'butter': {'carbs': 0.01, 'protein': 0.01, 'fat': 0.81, 'fiber': 0.00, 'calories': 717, 'sodium': 11},
    'ghee': {'carbs': 0.00, 'protein': 0.00, 'fat': 1.00, 'fiber': 0.00, 'calories': 900, 'sodium': 0},
    
    # Fruits
    'banana': {'carbs': 0.23, 'protein': 0.01, 'fat': 0.003, 'fiber': 0.03, 'calories': 89, 'sodium': 1},
    'apple': {'carbs': 0.14, 'protein': 0.003, 'fat': 0.004, 'fiber': 0.02, 'calories': 52, 'sodium': 1},
    'orange': {'carbs': 0.12, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.02, 'calories': 47, 'sodium': 0},
    'mango': {'carbs': 0.15, 'protein': 0.01, 'fat': 0.004, 'fiber': 0.02, 'calories': 60, 'sodium': 1},
    'grapes': {'carbs': 0.18, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.01, 'calories': 62, 'sodium': 2},
    'papaya': {'carbs': 0.11, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.02, 'calories': 43, 'sodium': 8},
    'pomegranate': {'carbs': 0.19, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.04, 'calories': 83, 'sodium': 3},
    'guava': {'carbs': 0.14, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.05, 'calories': 68, 'sodium': 2},
    
    # Nuts and Seeds
    'almonds': {'carbs': 0.22, 'protein': 0.21, 'fat': 0.50, 'fiber': 0.12, 'calories': 579, 'sodium': 1},
    'cashews': {'carbs': 0.30, 'protein': 0.18, 'fat': 0.44, 'fiber': 0.03, 'calories': 553, 'sodium': 12},
    'peanuts': {'carbs': 0.16, 'protein': 0.26, 'fat': 0.49, 'fiber': 0.08, 'calories': 567, 'sodium': 18},
    'walnuts': {'carbs': 0.14, 'protein': 0.15, 'fat': 0.65, 'fiber': 0.07, 'calories': 654, 'sodium': 2},
    'sesame seeds': {'carbs': 0.23, 'protein': 0.18, 'fat': 0.50, 'fiber': 0.12, 'calories': 573, 'sodium': 11},
    
    # Spices and Condiments
    'turmeric': {'carbs': 0.65, 'protein': 0.08, 'fat': 0.10, 'fiber': 0.21, 'calories': 354, 'sodium': 38},
    'cumin': {'carbs': 0.44, 'protein': 0.18, 'fat': 0.22, 'fiber': 0.11, 'calories': 375, 'sodium': 168},
    'coriander': {'carbs': 0.55, 'protein': 0.12, 'fat': 0.17, 'fiber': 0.42, 'calories': 298, 'sodium': 35},
    'garlic': {'carbs': 0.33, 'protein': 0.06, 'fat': 0.01, 'fiber': 0.02, 'calories': 149, 'sodium': 17},
    'ginger': {'carbs': 0.18, 'protein': 0.02, 'fat': 0.01, 'fiber': 0.02, 'calories': 80, 'sodium': 13},
    'chili': {'carbs': 0.09, 'protein': 0.02, 'fat': 0.01, 'fiber': 0.03, 'calories': 40, 'sodium': 7},
    'salt': {'carbs': 0.00, 'protein': 0.00, 'fat': 0.00, 'fiber': 0.00, 'calories': 0, 'sodium': 38758},
    'sugar': {'carbs': 1.00, 'protein': 0.00, 'fat': 0.00, 'fiber': 0.00, 'calories': 387, 'sodium': 1},
    'oil': {'carbs': 0.00, 'protein': 0.00, 'fat': 1.00, 'fiber': 0.00, 'calories': 884, 'sodium': 0},
    
    # Beverages
    'water': {'carbs': 0.00, 'protein': 0.00, 'fat': 0.00, 'fiber': 0.00, 'calories': 0, 'sodium': 7},
    'tea': {'carbs': 0.00, 'protein': 0.00, 'fat': 0.00, 'fiber': 0.00, 'calories': 1, 'sodium': 4},
    'coffee': {'carbs': 0.00, 'protein': 0.00, 'fat': 0.00, 'fiber': 0.00, 'calories': 2, 'sodium': 5},
    'juice': {'carbs': 0.12, 'protein': 0.01, 'fat': 0.001, 'fiber': 0.01, 'calories': 45, 'sodium': 4},
    'soft drink': {'carbs': 0.10, 'protein': 0.00, 'fat': 0.00, 'fiber': 0.00, 'calories': 42, 'sodium': 4},
    'lassi': {'carbs': 0.08, 'protein': 0.03, 'fat': 0.02, 'fiber': 0.00, 'calories': 50, 'sodium': 20},
    
    # Snacks and Sweets
    'samosa': {'carbs': 0.35, 'protein': 0.05, 'fat': 0.25, 'fiber': 0.02, 'calories': 308, 'sodium': 400},
    'pakora': {'carbs': 0.20, 'protein': 0.08, 'fat': 0.15, 'fiber': 0.02, 'calories': 200, 'sodium': 300},
    'biscuit': {'carbs': 0.70, 'protein': 0.08, 'fat': 0.15, 'fiber': 0.02, 'calories': 400, 'sodium': 200},
    'chips': {'carbs': 0.50, 'protein': 0.06, 'fat': 0.35, 'fiber': 0.04, 'calories': 536, 'sodium': 500},
    'sweet': {'carbs': 0.80, 'protein': 0.05, 'fat': 0.10, 'fiber': 0.01, 'calories': 400, 'sodium': 50},
    'halwa': {'carbs': 0.60, 'protein': 0.05, 'fat': 0.20, 'fiber': 0.02, 'calories': 400, 'sodium': 30},
    'kheer': {'carbs': 0.25, 'protein': 0.05, 'fat': 0.08, 'fiber': 0.01, 'calories': 150, 'sodium': 20},
}

def normalize_food_name(food_name: str) -> str:
    """Normalize food name for better matching"""
    # Convert to lowercase and remove extra spaces
    food_name = food_name.lower().strip()
    
    # Remove common prefixes and suffixes
    food_name = re.sub(r'^(the|a|an)\s+', '', food_name)
    food_name = re.sub(r'\s+(curry|masala|fry|fried|boiled|steamed|roasted|grilled)$', '', food_name)
    
    # Handle common variations
    variations = {
        'roti': ['chapati', 'phulka'],
        'dal': ['lentil', 'pulse'],
        'curd': ['yogurt', 'dahi'],
        'paneer': ['cottage cheese'],
        'ghee': ['clarified butter'],
        'brinjal': ['eggplant', 'aubergine'],
        'okra': ['lady finger', 'bhindi'],
        'bitter gourd': ['karela'],
        'bottle gourd': ['lauki', 'dudhi'],
        'ridge gourd': ['turai'],
        'green beans': ['french beans', 'sem'],
        'peas': ['matar'],
        'corn': ['makka', 'maize'],
        'chicken': ['murgh'],
        'mutton': ['goat meat', 'bakra'],
        'fish': ['machli'],
        'prawns': ['jhinga', 'shrimp'],
        'egg': ['anda'],
        'milk': ['dudh'],
        'banana': ['kela'],
        'apple': ['seb'],
        'orange': ['santra'],
        'mango': ['aam'],
        'grapes': ['angur'],
        'papaya': ['papita'],
        'pomegranate': ['anaar'],
        'guava': ['amrood'],
        'almonds': ['badam'],
        'cashews': ['kaju'],
        'peanuts': ['moongphali'],
        'walnuts': ['akhrot'],
        'sesame seeds': ['til'],
        'turmeric': ['haldi'],
        'cumin': ['jeera'],
        'coriander': ['dhaniya'],
        'garlic': ['lehsun'],
        'ginger': ['adrak'],
        'chili': ['mirchi'],
        'salt': ['namak'],
        'sugar': ['chini', 'shakkar'],
        'oil': ['tel'],
        'tea': ['chai'],
        'coffee': ['kaffee'],
        'juice': ['ras'],
        'soft drink': ['cold drink', 'soda'],
        'lassi': ['buttermilk'],
        'samosa': ['samosa'],
        'pakora': ['bhajiya', 'fritter'],
        'biscuit': ['cookie'],
        'chips': ['namkeen'],
        'sweet': ['mithai', 'dessert'],
        'halwa': ['halwa'],
        'kheer': ['rice pudding']
    }
    
    # Check for variations
    for standard_name, variants in variations.items():
        if food_name in variants or any(variant in food_name for variant in variants):
            return standard_name
    
    return food_name

def extract_food_items(text: str) -> List[str]:
    """Extract food items from text description"""
    # Split by common separators
    items = re.split(r'[,;|&+]', text.lower())
    
    # Clean and normalize each item
    food_items = []
    for item in items:
        item = item.strip()
        if item:
            # Remove quantity indicators
            item = re.sub(r'^\d+\s*', '', item)  # Remove leading numbers
            item = re.sub(r'\s*\d+\s*$', '', item)  # Remove trailing numbers
            item = re.sub(r'\s*(pieces?|pcs?|grams?|g|kg|cups?|bowls?|plates?|servings?)\s*', ' ', item)
            item = item.strip()
            
            if item and len(item) > 1:
                food_items.append(item)
    
    return food_items

def find_matching_foods(food_items: List[str]) -> List[Tuple[str, str, Dict]]:
    """Find matching foods in database"""
    matches = []
    
    for item in food_items:
        normalized_item = normalize_food_name(item)
        
        # Direct match
        if normalized_item in FOOD_DATABASE:
            matches.append((item, normalized_item, FOOD_DATABASE[normalized_item]))
            continue
        
        # Partial match
        for db_item, nutrition in FOOD_DATABASE.items():
            if (normalized_item in db_item or 
                db_item in normalized_item or
                any(word in db_item for word in normalized_item.split() if len(word) > 2)):
                matches.append((item, db_item, nutrition))
                break
    
    return matches

def calculate_nutrition_totals(matches: List[Tuple[str, str, Dict]], portion_size: str = 'medium') -> Dict:
    """Calculate total nutrition based on portion size"""
    # Portion size multipliers
    portion_multipliers = {
        'small': 0.7,
        'medium': 1.0,
        'large': 1.5
    }
    
    multiplier = portion_multipliers.get(portion_size, 1.0)
    
    # Initialize totals
    totals = {
        'carbs': 0,
        'protein': 0,
        'fat': 0,
        'fiber': 0,
        'calories': 0,
        'sodium': 0
    }
    
    # Sum up nutrition from all matched foods
    for original_item, matched_item, nutrition in matches:
        for nutrient, value in nutrition.items():
            if nutrient in totals:
                totals[nutrient] += value * multiplier
    
    # Convert to percentages for macronutrients
    total_macros = totals['carbs'] + totals['protein'] + totals['fat']
    if total_macros > 0:
        totals['carbs'] = totals['carbs'] / total_macros
        totals['protein'] = totals['protein'] / total_macros
        totals['fat'] = totals['fat'] / total_macros
    
    return totals

def analyze_food_items(food_text: str, portion_size: str = 'medium') -> Dict:
    """Main function to analyze food items and return nutritional breakdown"""
    # Extract food items from text
    food_items = extract_food_items(food_text)
    
    # Find matching foods in database
    matches = find_matching_foods(food_items)
    
    # Calculate nutrition totals
    nutrition = calculate_nutrition_totals(matches, portion_size)
    
    # Prepare response
    response = {
        'food_items': food_items,
        'matched_items': [match[1] for match in matches],
        'nutrition': nutrition,
        'analysis': {
            'total_items_found': len(matches),
            'total_items_searched': len(food_items),
            'match_rate': len(matches) / len(food_items) if food_items else 0
        }
    }
    
    return response

# Test function
if __name__ == "__main__":
    # Test the food analysis
    test_text = "2 rotis, dal, rice, chicken curry"
    result = analyze_food_items(test_text, 'medium')
    print("Food Analysis Result:")
    print(f"Input: {test_text}")
    print(f"Extracted items: {result['food_items']}")
    print(f"Matched items: {result['matched_items']}")
    print(f"Nutrition: {result['nutrition']}")
    print(f"Analysis: {result['analysis']}")


