import random
import datetime
import numpy as np
import csv
import json
from pathlib import Path
from data_bank_profiles_config import (
    income_profiles,
    transaction_categories,
    consumption_profile
)
from faker import Faker

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
fake = Faker(['es_ES'])

# List of municipalities in the Basque Country
cities = [
    "Bilbao", "Barakaldo", "Getxo", "Portugalete", "Santurtzi", "Basauri", "Leioa", 
    "Galdakao", "Sestao", "Durango", "Erandio", "Bermeo", "Mungia", "Sopela", "Berango",
    "San Sebastian", "Irun", "Errenteria", "Eibar", "Zarautz", "Arrasate/Mondragon", 
    "Hernani", "Lasarte-Oria", "Hondarribia", "Pasaia", "Andoain",
    "Vitoria-Gasteiz", "Llodio", "Amurrio", "Salvatierra/Agurain", "Oyón-Oion", 
    "Iruña de Oca", "Alegría-Dulantzi", "Zuia", "Labastida/Bastida", "Elciego"
]

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

@app.get("/")
def read_root():
    """API entry point"""
    return "Welcome to the Bank Transaction Generation API!"

def generate_transactions(profile:str, from_date:datetime.datetime):
    """Generates transactions based on the indicated profile"""
    if profile not in income_profiles:
        raise ValueError("Unknown profile")

    profile_data = income_profiles[profile]
    customer_name = fake.name()
    account_name = fake.iban()
    transaction_city = "Bilbao"  # Fixed city for housing transactions

    salary = round_to_cents(random.uniform(profile_data["salary"][0], profile_data["salary"][1]))
    partner_salary = 0
    if profile_data['has_partner'] and profile_data['partner_works']:
        partner_salary = round_to_cents(random.uniform(profile_data["salary"][0], profile_data["salary"][1]))

    balance = round_to_cents(random.uniform(
        profile_data['initial_balance_range'][0],
        profile_data['initial_balance_range'][1]
    ))

    to_date = datetime.datetime.now()

    idx = 1
    transactions = []
    current_date = from_date
    housing_expense = round_to_cents(random.uniform(*consumption_profile["monthly"]["housing"][1 if profile_data['owns_house'] else 0]["range"]))
    
    # New variables for extra income
    months_since_last_extra_income = 0
    extra_income_amount = round_to_cents(salary * 0.1)

    while current_date <= to_date:
        # Monthly salary (or salaries)
        if current_date.day == 1:
            timestamp = generate_timestamp(current_date)
            balance += salary
            transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
            transaction = {
                'profile': profile,
                'customer': customer_name,
                'account': account_name,
                'transaction_ref_id': transaction_ref_id,
                'timestamp': timestamp.isoformat(),
                'city': transaction_city,
                'transaction_type': "transfer",
                'transaction_category': "Salary",
                'amount_eur': salary,
                'balance': balance
            }
            transactions.append(transaction)
            idx += 1

            if partner_salary > 0:
                balance += partner_salary
                transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                transaction = {
                    'profile': profile,
                    'customer': customer_name,
                    'account': account_name,
                    'transaction_ref_id': transaction_ref_id,
                    'timestamp': timestamp.isoformat(),
                    'city': transaction_city,
                    'transaction_type': "transfer",
                    'transaction_category': "Partner Salary",
                    'amount_eur': partner_salary,
                    'balance': balance
                }
                transactions.append(transaction)
                idx += 1

            # Extra income every 2-3 months
            months_since_last_extra_income += 1
            if months_since_last_extra_income >= random.randint(2, 3):
                balance += extra_income_amount
                transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                transaction = {
                    'profile': profile,
                    'customer': customer_name,
                    'account': account_name,
                    'transaction_ref_id': transaction_ref_id,
                    'timestamp': timestamp.isoformat(),
                    'city': transaction_city,
                    'transaction_type': "transfer",
                    'transaction_category': "Extra Income",
                    'amount_eur': extra_income_amount,
                    'balance': balance
                }
                transactions.append(transaction)
                idx += 1
                months_since_last_extra_income = 0

            # Bonus in June and December
            if current_date.month in [6, 12]:
                bonus = round_to_cents(random.uniform(0.9 * salary, 1.1 * salary))
                balance += bonus
                transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                transaction = {
                    'profile': profile,
                    'customer': customer_name,
                    'account': account_name,
                    'transaction_ref_id': transaction_ref_id,
                    'timestamp': timestamp.isoformat(),
                    'city': transaction_city,
                    'transaction_type': "transfer",
                    'transaction_category': "Bonus",
                    'amount_eur': bonus,
                    'balance': balance
                }
                transactions.append(transaction)
                idx += 1

        # Rent or Mortgage (5th of each month)
        if current_date.day == 5:
            timestamp = generate_timestamp(current_date)
            balance -= housing_expense
            transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
            transaction = {
                'profile': profile,
                'customer': customer_name,
                'account': account_name,
                'transaction_ref_id': transaction_ref_id,
                'timestamp': timestamp.isoformat(),
                'city': "Bilbao",
                'transaction_type': "Housing",
                'transaction_category': "Mortgage" if profile_data['owns_house'] else "Rent",
                'amount_eur': -housing_expense,
                'balance': balance
            }
            transactions.append(transaction)
            idx += 1

        # Utility bills (5th, 6th, or 7th of each month)
        if current_date.day in [5, 6, 7]:
            for service in consumption_profile["monthly"]["basic_services"]:
                if random.random() < 0.33:  # Distribute bills across the 3 days
                    timestamp = generate_timestamp(current_date)
                    bill_amount = round_to_cents(random.uniform(*service["range"]))
                    balance -= bill_amount
                    transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                    transaction = {
                        'profile': profile,
                        'customer': customer_name,
                        'account': account_name,
                        'transaction_ref_id': transaction_ref_id,
                        'timestamp': timestamp.isoformat(),
                        'city': "Bilbao",
                        'transaction_type': "Basic services",
                        'transaction_category': service["concept"],
                        'amount_eur': -bill_amount,
                        'balance': balance
                    }
                    transactions.append(transaction)
                    idx += 1

        # Other transactions based on frequency
        for category in consumption_profile["frequent"] + consumption_profile["occasional"]:
            if random.random() < (category["frequency"] / 30):  # Adjust frequency to daily probability
                timestamp = generate_timestamp(current_date)
                transaction_amount = round_to_cents(random.uniform(*category["range"]))
                balance -= transaction_amount
                transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                transaction = {
                    'profile': profile,
                    'customer': customer_name,
                    'account': account_name,
                    'transaction_ref_id': transaction_ref_id,
                    'timestamp': timestamp.isoformat(),
                    'city': "Bilbao" if random.random() < 0.8 else random.choice(cities),
                    'transaction_type': "Expense",
                    'transaction_category': category["concept"],
                    'amount_eur': -transaction_amount,
                    'balance': balance
                }
                transactions.append(transaction)
                idx += 1

        # Conditional expenses based on profile attributes
        for category in consumption_profile["conditional"]:
            if category["concept"] == "children":
                if profile_data['children'] > 0 and random.random() < (category["frequency"] / 30):
                    timestamp = generate_timestamp(current_date)
                    transaction_amount = round_to_cents(random.uniform(*category["range"]) * profile_data['children'] * category["multiplier"])
                    balance -= transaction_amount
                    transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                    transaction = {
                        'profile': profile,
                        'customer': customer_name,
                        'account': account_name,
                        'transaction_ref_id': transaction_ref_id,
                        'timestamp': timestamp.isoformat(),
                        'city': "Bilbao" if random.random() < 0.8 else random.choice(cities),
                        'transaction_type': "Expense",
                        'transaction_category': "Children expenses",
                        'amount_eur': -transaction_amount,
                        'balance': balance
                    }
                    transactions.append(transaction)
                    idx += 1
            elif (category["concept"] == "car" and profile_data['has_car']) or \
                 (category["concept"] == "pet" and profile_data['has_pet']):
                if random.random() < (category["frequency"] / 30):
                    timestamp = generate_timestamp(current_date)
                    transaction_amount = round_to_cents(random.uniform(*category["range"]))
                    balance -= transaction_amount
                    transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
                    transaction = {
                        'profile': profile,
                        'customer': customer_name,
                        'account': account_name,
                        'transaction_ref_id': transaction_ref_id,
                        'timestamp': timestamp.isoformat(),
                        'city': "Bilbao" if random.random() < 0.8 else random.choice(cities),
                        'transaction_type': "Expense",
                        'transaction_category': f"{category['concept'].capitalize()} expenses",
                        'amount_eur': -transaction_amount,
                        'balance': balance
                    }
                    transactions.append(transaction)
                    idx += 1

        # Minor daily expenses
        if random.random() < 0.7:  # 70% chance of minor expense each day
            timestamp = generate_timestamp(current_date)
            minor_expense = round_to_cents(random.uniform(3, 10))
            balance -= minor_expense
            transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
            transaction = {
                'profile': profile,
                'customer': customer_name,
                'account': account_name,
                'transaction_ref_id': transaction_ref_id,
                'timestamp': timestamp.isoformat(),
                'city': "Bilbao" if random.random() < 0.8 else random.choice(cities),
                'transaction_type': "Expense",
                'transaction_category': "Minor expenses",
                'amount_eur': -minor_expense,
                'balance': balance
            }
            transactions.append(transaction)
            idx += 1

        current_date += datetime.timedelta(days=1)

    # Sort transactions by timestamp
    transactions.sort(key=lambda x: x['timestamp'])

    # Save to CSV
    csv_path = save_to_csv(transactions)

    return {
        "transactions": transactions,
        "csv_path": str(csv_path),
        "transaction_count": len(transactions)
    }

@app.get("/transactions")
def gen_transactions(profile:str, from_date:str):
    """API endpoint for generating transactions"""
    try:
        from_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if profile not in income_profiles:
        raise HTTPException(status_code=400, detail="Unknown profile")

    data = generate_transactions(profile, from_date)
    return JSONResponse(content=data)

def save_to_csv(transactions):
    """Saves the transactions to a CSV file in the /data folder"""
    data_folder = Path(__file__).parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M")
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


if __name__ == "__main__":
    start_date = "2022-01-01"
    profile = "High income"
    data = generate_transactions(profile, datetime.datetime.strptime(start_date, "%Y-%m-%d"))
    
    for transaction in data['transactions'][:]:
        print(json.dumps(transaction, indent=2))
    
    # Save transactions to a JSON file
    json_folder = Path(__file__).parent.parent / "data"
    json_folder.mkdir(parents=True, exist_ok=True)
    json_filename = f"data_bank_trx_{datetime.datetime.now().strftime('%Y_%m_%d__%H_%M')}.json"
    json_filepath = json_folder / json_filename
    
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(data['transactions'], f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generated {data['transaction_count']} transactions")
    print(f"✅ CSV  file saved at: {data['csv_path']}")
    print(f"✅ JSON file saved at: {json_filepath}")