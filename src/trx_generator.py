import random
from datetime import datetime, timedelta
from faker import Faker
from utils import generate_timestamp, round_to_cents
from config import buyer_profiles, consumption_profile, cities, trx_cat

fake = Faker(['es_ES'])

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

def generate_trxs(profile_data: dict, from_date: datetime):
    customer_name = profile_data['name']
    account_name = profile_data['iban']
    trx_city = profile_data['city']

    salary = round_to_cents(random.uniform(*profile_data["salary"]))

    partner_salary = 0
    if profile_data['has_partner'] and profile_data['partner_works']:
        partner_salary = round_to_cents(random.uniform(profile_data["salary"][0] * 0.8, profile_data["salary"][1] * 1.1))

    balance = round_to_cents(random.uniform(*profile_data['initial_balance_range']))

    to_date = datetime.now()
    idx = 1
    trxs = []
    current_date = from_date
    
    housing_expense = round_to_cents(random.uniform(*consumption_profile["monthly"]["housing"][1 if profile_data['owns_house'] else 0]["range"]))

    months_since_last_extra_income = 0
    extra_income_amount = round_to_cents(salary * 0.1)

    while current_date <= to_date:
        # Monthly salary (or salaries)
        if current_date.day == 1:
            timestamp = generate_timestamp(current_date)
            balance += salary
            trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary", salary, balance))
            idx += 1

            if partner_salary > 0:
                balance += partner_salary
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_partner", partner_salary, balance))
                idx += 1

            # Extra income every 2-3 months
            months_since_last_extra_income += 1
            if months_since_last_extra_income >= random.randint(2, 3):
                balance += extra_income_amount
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "extra_income", extra_income_amount, balance))
                idx += 1
                months_since_last_extra_income = 0

            # Bonus in June and December
            if current_date.month in [6, 12]:
                bonus = round_to_cents(random.uniform(0.7 * salary, 0.8 * salary))
                balance += bonus
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_extra", bonus, balance))
                idx += 1

                if partner_salary > 0:
                    bonus_partner = round_to_cents(random.uniform(0.7 * partner_salary, 0.8 * partner_salary))
                    balance += bonus_partner
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_partner_extra", bonus_partner, balance))
                    idx += 1

        # Rent or Mortgage (5th of each month)
        if current_date.day == 5:
            timestamp = generate_timestamp(current_date)
            balance -= housing_expense
            trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "Housing", "Mortgage" if profile_data['owns_house'] else "Rent", -housing_expense, balance))
            idx += 1

        # Utility bills (5th, 6th, or 7th of each month)
        if current_date.day in [5, 6, 7]:
            for service in consumption_profile["monthly"]["basic_services"]:
                if random.random() < 0.33:  # Distribute bills across the 3 days
                    timestamp = generate_timestamp(current_date)
                    bill_amount = round_to_cents(random.uniform(*service["range"]))
                    balance -= bill_amount
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "basic_services", service["concept"], -bill_amount, balance))
                    idx += 1

        # Other trxs based on frequency and weights
        for _ in range(profile_data['trx_frequency']):
            if random.random() < sum(profile_data['trx_weights']):
                timestamp = generate_timestamp(current_date)
                trx_amount = round_to_cents(random.uniform(*profile_data['trx_range']))
                balance -= trx_amount
                category = random.choices(consumption_profile["frequent"] + consumption_profile["occasional"], 
                                          weights=[cat["frequency"] for cat in consumption_profile["frequent"] + consumption_profile["occasional"]])[0]
                trx_category = random.choice(trx_cat)  # Using trx_cat from config
                trxs.append(generate_transaction(customer_name, account_name, 
                                                 trx_city if random.random() < 0.8 else random.choice(cities), 
                                                 idx, timestamp, "Expense", trx_category, -trx_amount, balance))
                idx += 1

        # Conditional expenses
        for condition in consumption_profile["conditional"]:
            if condition["concept"] == "children" and profile_data["children"] > 0:
                if random.random() < condition["frequency"]:
                    timestamp = generate_timestamp(current_date)
                    child_expense = round_to_cents(random.uniform(*condition["range"]) * profile_data["children"] * condition["multiplier"])
                    balance -= child_expense
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "Expense", "Children", -child_expense, balance))
                    idx += 1
            elif condition["concept"] == "car" and profile_data["has_car"]:
                if random.random() < condition["frequency"]:
                    timestamp = generate_timestamp(current_date)
                    car_expense = round_to_cents(random.uniform(*condition["range"]))
                    balance -= car_expense
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "Expense", "Car", -car_expense, balance))
                    idx += 1

        # Advance to the next day
        current_date += timedelta(days=1)

    trxs.sort(key=lambda x: x['trx_id'])

    return {
        "trxs": trxs,
        "trx_count": len(trxs)
    }