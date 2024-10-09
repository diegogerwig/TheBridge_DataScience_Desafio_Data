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

def save_to_csv(trxs, filename):
    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)
    filepath = data_folder / f"{filename}.csv"

    fieldnames = ['profile', 'name', 'surname', 'birth_date', 'iban', 'trx_id', 'timestamp', 'city',
                  'trx_type', 'trx_cat', 'amount_eur', 'balance']

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for trx in trxs:
            if 'balance' in trx:
                trx['balance'] = round(trx['balance'], 2)
            row = {field: trx.get(field, '') for field in fieldnames}
            writer.writerow(row)

    return str(filepath.resolve())

def calculate_iban_control_digits(bank_code, branch_code, account_number):
    
    iban = f"{bank_code}{branch_code}{account_number}142800"
    
    iban = ''.join(str(ord(char) - 55) if char.isalpha() else char for char in iban)
    
    remainder = int(iban) % 97
    
    control_digits = 98 - remainder
    
    return f"{control_digits:02d}"

def generate_spanish_dni():
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    
    letter_map = "TRWAGMYFPDXBNJZSQVHLCKE"
    control_letter = letter_map[int(numbers) % 23]
    
    dni = numbers + control_letter
    
    return dni