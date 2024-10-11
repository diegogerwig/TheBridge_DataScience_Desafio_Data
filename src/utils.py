import random
from pathlib import Path
import csv
from faker import Faker
from unidecode import unidecode

adjectives = ['cool', 'super', 'hyper', 'mega', 'ultra', 'extreme', 'awesome', 'brilliant', 'clever', 'smart']
nouns = ['tech', 'web', 'net', 'code', 'dev', 'app', 'cloud', 'data', 'byte', 'pixel']
tlds = ['.com', '.net', '.org', '.io', '.tech', '.app', '.co', '.digital', '.online', '.site']

fake = Faker(['es_ES'])

def get_transaction_city(residence_city, nearby_cities, transaction_type):
    rand = random.random()
    if transaction_type == "expenses":
        if rand < 0.7:
            return residence_city
        elif rand < 0.95 and nearby_cities:
            return random.choice(nearby_cities)
        else:
            return fake.city()
    else:  # Para ingresos
        if rand < 0.999:
            return residence_city
        elif nearby_cities:
            return random.choice(nearby_cities)
        else:
            return fake.city()

def generate_transaction(customer_name, account_name, trx_city, idx, timestamp, trx_type, trx_cat, amount, balance):
    trx_id = f"TRX_N-{str(idx).zfill(5)}-{str(fake.unique.random_number(digits=8)).zfill(8)}"
    return {
        'customer': customer_name,
        'account': account_name,
        'trx_id': trx_id,
        'timestamp': timestamp.isoformat(),
        'city': trx_city,
        'trx_type': trx_type,
        'trx_cat': trx_cat,
        'amount_eur': amount,
        'balance': balance
    }

def adjust_range(range_tuple, salary, index):
    min_value, max_value = range_tuple
    adjusted_min = min_value * (salary / 2000) * index  # Assuming 2000 is a reference salary
    adjusted_max = max_value * (salary / 2000) * index
    return (adjusted_min, adjusted_max)


def generate_random_domain():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    tld = random.choice(tlds)
    return f"{adjective}{noun}{tld}"


def generate_email(name, surname):
    domain = generate_random_domain()
    name = unidecode(name)
    surname = unidecode(surname)
    return f"{name.lower()}.{surname.lower()}@{domain}"


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


def generate_password(length):
    digits = '0123456789'
    
    password = ''.join(random.choice(digits) for _ in range(length))
    
    return password
