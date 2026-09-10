from django.core.exceptions import ValidationError

def validate_coffee_price(value):
    """التحقق من أن سعر صنف القهوة منطقي وليس سالباً أو صفراً."""
    if value <= 0:
        raise ValidationError("سعر القهوة يجب أن يكون أكبر من الصفر.")

def validate_roast_level(value):
    """التحقق من أن مستوى التحميص ينتمي للأنواع المعتمدة فقط."""
    valid_levels = ['Light', 'Medium', 'Dark']
    if value not in valid_levels:
        raise ValidationError("مستوى التحميص يجب أن يكون إحدى القيم التالية: Light, Medium, Dark")