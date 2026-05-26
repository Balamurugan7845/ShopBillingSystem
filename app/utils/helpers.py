import datetime
import random
import string

def generate_bill_number():
    """Generate a unique bill number based on timestamp"""
    today = datetime.datetime.now()
    # Format: BILLYYYYMMDDHHMMSS + random 3 digits for uniqueness
    timestamp = today.strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(random.choices(string.digits, k=3))
    return f"BILL{timestamp}{random_suffix}"

def format_currency(amount):
    """Format amount as currency with ₹ symbol"""
    try:
        return f"₹{float(amount):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

def calculate_gst(amount, gst_rate=18):
    """Calculate GST amount"""
    try:
        return (float(amount) * gst_rate) / 100
    except (ValueError, TypeError):
        return 0.0

def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Simple phone number validation"""
    import re
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone) is not None

def get_current_timestamp():
    """Get current timestamp in various formats"""
    now = datetime.datetime.now()
    return {
        'datetime': now,
        'date': now.strftime('%Y-%m-%d'),
        'time': now.strftime('%H:%M:%S'),
        'datetime_str': now.strftime('%Y-%m-%d %H:%M:%S')
    }

def generate_invoice_number():
    """Generate a unique invoice number"""
    today = datetime.datetime.now()
    date_part = today.strftime('%Y%m')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"INV{date_part}{random_part}"

def calculate_discount(amount, discount_type, discount_value):
    """Calculate discount amount based on type"""
    try:
        amount = float(amount)
        if discount_type == 'percentage':
            return (amount * float(discount_value)) / 100
        elif discount_type == 'fixed':
            return float(discount_value)
        else:
            return 0.0
    except (ValueError, TypeError):
        return 0.0

def parse_date(date_str):
    """Parse date string to datetime object"""
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y%m%d']
    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None