def validate_and_parse_inputs(weight_str, height_str):
    """
    Validates user input strings and converts them to positive floats.
    Raises ValueError with context-specific messages.
    """
    if not weight_str.strip() or not height_str.strip():
        raise ValueError("Weight and Height fields cannot be empty.")
    
    try:
        weight = float(weight_str)
    except ValueError:
        raise ValueError("Weight must be a valid number (e.g., 70.5).")
        
    try:
        height = float(height_str)
    except ValueError:
        raise ValueError("Height must be a valid number (e.g., 1.75).")
        
    if weight <= 0:
        raise ValueError("Weight must be greater than 0.")
    if height <= 0:
        raise ValueError("Height must be greater than 0.")
    if height > 3.0:
        raise ValueError("Height seems too large. Please enter height in meters (e.g., 1.75).")

    return weight, height

def calculate_bmi(weight, height):
    """Calculates BMI and returns (rounded_bmi, category, hex_color)."""
    bmi = round(weight / (height ** 2), 2)
    
    if bmi < 18.5:
        category = "Underweight"
        color = "#3498db"  # Blue
    elif 18.5 <= bmi <= 24.9:
        category = "Normal Weight"
        color = "#2ecc71"  # Green
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight"
        color = "#f39c12"  # Orange
    else:
        category = "Obese"
        color = "#e74c3c"  # Red
        
    return bmi, category, color