import random
from datetime import datetime

def generate_timestamp(date):
    """Generates a timestamp with a random hour, preferably during daytime"""
    if random.random() < 0.85:  # 85% chance of daytime hours
        hour = random.randint(8, 20)
    else:
        hour = random.randint(0, 7) if random.random() < 0.5 else random.randint(21, 23)
    
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return date.replace(hour=hour, minute=minute, second=second)

def round_to_cents(amount):
    """Rounds the given amount to 2 decimal places"""
    return round(amount, 2)
