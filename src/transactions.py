import random
from datetime import datetime, timedelta
from faker import Faker
from utils import generate_timestamp, round_to_cents
from config import income_profiles, consumption_profile, cities

fake = Faker(['es_ES'])

def generate_transactions(profile: str, from_date: datetime):
    if profile not in income_profiles:
        raise ValueError("Unknown profile")

    profile_data = income_profiles[profile]
    customer_name = fake.name()
    account_name = fake.iban()
    transaction_city = "Bilbao"

    salary = round_to_cents(random.uniform(profile_data["salary"][0], profile_data["salary"][1]))
    partner_salary = 0
    if profile_data['has_partner'] and profile_data['partner_works']:
        partner_salary = round_to_cents(random.uniform(profile_data["salary"][0], profile_data["salary"][1]))

    balance = round_to_cents(random.uniform(
        profile_data['initial_balance_range'][0],
        profile_data['initial_balance_range'][1]
    ))

    to_date = datetime.now()

    idx = 1
    transactions = []
    current_date = from_date
    housing_expense = round_to_cents(random.uniform(*consumption_profile["monthly"]["housing"][1 if profile_data['owns_house'] else 0]["range"]))

    months_since_last_extra_income = 0
    extra_income_amount = round_to_cents(salary * 0.1)

    while current_date <= to_date:
        # Monthly salary (or salaries)
        if current_date.day == 1:
            timestamp = generate_timestamp(current_date)
            balance += salary
            transaction_ref_id = f"TXN-{fake.unique.random_number(digits=8)}-{idx}"
            transaction = {
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

        # Advance to the next day
        current_date += timedelta(days=1)

    transactions.sort(key=lambda x: x['timestamp'])

    return {
        "transactions": transactions,
        "transaction_count": len(transactions)
    }