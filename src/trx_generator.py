import random
from datetime import datetime, timedelta
from faker import Faker
from utils import generate_timestamp, round_to_cents
from config import consumption_profile, cities
fake = Faker(['es_ES'])

billed_services = {}
annual_bills_paid = {}

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
    global billed_services, annual_bills_paid
    customer_name = profile_data['name']
    account_name = profile_data['iban']
    trx_city = profile_data['city']

    initial_salary = round_to_cents(random.uniform(*profile_data["salary"]))
    salary = initial_salary

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
    extra_income_amount = round_to_cents(random.uniform(0.1 * salary, 0.2 * salary))

    last_salary_increase_year = from_date.year - 1

    while current_date <= to_date:
        # Annual salary increase (2-4%) on the first day of each year
        if current_date.month == 1 and current_date.day == 1 and current_date.year > last_salary_increase_year:
            increase_rate = random.uniform(0.02, 0.04)  # 2-4% increase
            salary = round_to_cents(salary * (1 + increase_rate))
            if partner_salary > 0:
                partner_salary = round_to_cents(partner_salary * (1 + increase_rate))
            last_salary_increase_year = current_date.year

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

            # Extra income every 3-4 months
            months_since_last_extra_income += 1
            if months_since_last_extra_income >= random.randint(3, 4):
                balance += extra_income_amount
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "extra_income", extra_income_amount, balance))
                idx += 1
                months_since_last_extra_income = 0

            # Bonus in June and December
            if current_date.month in [6, 12]:
                bonus = round_to_cents(random.uniform(0.7 * salary, 0.8 * salary))
                balance += bonus
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_bonus", bonus, balance))
                idx += 1

                if partner_salary > 0:
                    bonus_partner = round_to_cents(random.uniform(0.7 * partner_salary, 0.8 * partner_salary))
                    balance += bonus_partner
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_partner_bonus", bonus_partner, balance))
                    idx += 1

        # Rent or Mortgage (5th of each month)
        if current_date.day == 4:
            timestamp = generate_timestamp(current_date)
            balance -= housing_expense
            trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", "mortgage" if profile_data['owns_house'] else "rent", -housing_expense, balance))
            idx += 1

        # Annual bills (taxes and insurance in June or July)
        if current_date.month in [6, 7]:
            year_key = current_date.year
            if year_key not in annual_bills_paid:
                annual_bills_paid[year_key] = False

            if not annual_bills_paid[year_key]:
                # 50% chance to bill in June, otherwise it will be billed in July
                if current_date.month == 7 or (current_date.month == 6 and random.random() < 0.5):
                    for annual_bill in consumption_profile["annual"]:
                        timestamp = generate_timestamp(current_date)
                        bill_amount = round_to_cents(random.uniform(*annual_bill["range"]))
                        balance -= bill_amount
                        trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", annual_bill["concept"], -bill_amount, balance))
                        idx += 1
                    
                    annual_bills_paid[year_key] = True

        # Utility bills (randomly distributed between 5th and 8th of each month)
        if 5 <= current_date.day <= 8:
            global billed_services
            
            # Initialize billed_services for this month if it's not already set
            month_key = f"{current_date.year}-{current_date.month}"
            if month_key not in billed_services:
                billed_services[month_key] = {service['concept']: False for service in consumption_profile["monthly"]["basic_services"]}
            
            for service in consumption_profile["monthly"]["basic_services"]:
                # If this service hasn't been billed yet this month
                if not billed_services[month_key][service['concept']]:
                    # 25% chance each day to bill this service
                    if random.random() < 0.25:
                        timestamp = generate_timestamp(current_date)
                        bill_amount = round_to_cents(random.uniform(*service["range"]))
                        balance -= bill_amount
                        trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", service["concept"], -bill_amount, balance))
                        idx += 1
                        # Mark this service as billed
                        billed_services[month_key][service['concept']] = True
            
            # If it's the 8th and some services haven't been billed, bill them now
            if current_date.day == 8:
                for service in consumption_profile["monthly"]["basic_services"]:
                    if not billed_services[month_key][service['concept']]:
                        timestamp = generate_timestamp(current_date)
                        bill_amount = round_to_cents(random.uniform(*service["range"]))
                        balance -= bill_amount
                        trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", service["concept"], -bill_amount, balance))
                        idx += 1
                
                # Clear the billed_services for this month
                del billed_services[month_key]

        all_categories = consumption_profile["frequent"] + consumption_profile["occasional"]
        
        for category in all_categories:
            if random.random() < category["frequency"]:
                timestamp = generate_timestamp(current_date)
                trx_amount = round_to_cents(random.uniform(*category['range']))
                balance -= trx_amount
                trx_category = category['concept']
                trxs.append(generate_transaction(
                    customer_name, 
                    account_name,
                    trx_city if random.random() < 0.8 else random.choice(cities),
                    idx, 
                    timestamp, 
                    "Expense", 
                    trx_category, 
                    -trx_amount, 
                    balance
                ))
                idx += 1

        # Conditional expenses
        for condition in consumption_profile["conditional"]:
            if condition["concept"] == "children" and profile_data["children"] > 0:
                if random.random() < condition["frequency"]:
                    timestamp = generate_timestamp(current_date)
                    base_child_expense = round_to_cents(random.uniform(*condition["range"]))
                    child_expense = base_child_expense * profile_data["children"]
                    
                    # Increase by 30% for each additional child
                    if profile_data["children"] > 1:
                        child_expense *= (1 + (profile_data["children"] - 1) * 0.3)
                    
                    child_expense = round_to_cents(child_expense)
                    balance -= child_expense
                    trxs.append(generate_transaction(
                        customer_name, 
                        account_name, 
                        trx_city, 
                        idx, 
                        timestamp, 
                        "expenses", 
                        "children", 
                        -child_expense, 
                        balance
                    ))
                    idx += 1
            if condition["concept"] == "car" and profile_data["has_car"]:
                if random.random() < condition["frequency"]:
                    timestamp = generate_timestamp(current_date)
                    car_expense = round_to_cents(random.uniform(*condition["range"]))
                    balance -= car_expense
                    trxs.append(generate_transaction(
                        customer_name, 
                        account_name, 
                        trx_city, 
                        idx, 
                        timestamp, 
                        "expenses", 
                        "car", 
                        -car_expense, 
                        balance
                    ))
                    idx += 1

        # Advance to the next day
        current_date += timedelta(days=1)

    trxs.sort(key=lambda x: x['trx_id'])

    return {
        "trxs": trxs,
        "trx_count": len(trxs)
    }