import random
from datetime import datetime
from pathlib import Path
import csv

def generate_timestamp(date):
    if random.random() < 0.85:
        hour = random.randint(8, 20)
    else:
        hour = random.randint(0, 7) if random.random() < 0.5 else random.randint(21, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return date.replace(hour=hour, minute=minute, second=second)

def round_to_cents(amount):
    return round(amount, 2)

def save_to_csv(transactions):
    data_folder = Path(__file__).parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M")
    filename = f"data_bank_trx_{timestamp}.csv"
    filepath = data_folder / filename

    fieldnames = ['profile', 'customer', 'account', 'transaction_ref_id', 'timestamp', 'city',
                  'transaction_type', 'transaction_category', 'amount_eur', 'balance']

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)

    return filepath
