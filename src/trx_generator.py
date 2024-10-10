import random
from datetime import datetime, timedelta
from utils import generate_timestamp, round_to_cents, get_transaction_city, generate_transaction, adjust_range
from config import consumption_profile


def generate_trxs(profile_data: dict, from_date: datetime, annual_bills_paid: dict):
    customer_name = profile_data['name']
    account_name = profile_data['iban']
    residence_city = profile_data['city']
    nearby_cities = profile_data.get('nearby_cities', [])  # Assuming nearby_cities is part of profile_data

    initial_salary = round_to_cents(random.uniform(*profile_data["salary"]))
    salary = initial_salary

    partner_salary = 0
    if profile_data['has_partner'] and profile_data['partner_works']:
        partner_salary = round_to_cents(random.uniform(profile_data["salary"][0] * 0.8, profile_data["salary"][1] * 1.1))

    total_salary = salary + partner_salary
    balance = round_to_cents(random.uniform(*profile_data['initial_assets']))

    to_date = datetime.now()
    idx = 1
    trxs = []
    current_date = from_date
    months_since_last_extra_income = 0
    extra_income_amount = round_to_cents(random.uniform(0.1 * salary, 0.2 * salary))

    # Adjust fixed expenses based on salary and index_fix_expenses
    index_fix = profile_data['index_fix_expenses']
    adjusted_housing_range = adjust_range(consumption_profile["monthly"]["housing"][1 if profile_data['owns_house'] else 0]["range"], total_salary, index_fix)
    housing_expense = round_to_cents(random.uniform(*adjusted_housing_range))

    # Calculate total fixed expenses
    total_fixed_expenses = housing_expense
    for service in consumption_profile["monthly"]["basic_services"]:
        adjusted_range = adjust_range(service["range"], total_salary, index_fix)
        total_fixed_expenses += round_to_cents(random.uniform(*adjusted_range))
    for annual_bill in consumption_profile["annual"]:
        adjusted_range = adjust_range(annual_bill["range"], total_salary, index_fix)
        total_fixed_expenses += round_to_cents(random.uniform(*adjusted_range)) / 12  # Divide by 12 to get monthly equivalent

    # Calculate available money for variable expenses
    available_money = total_salary - total_fixed_expenses

    last_salary_increase_year = from_date.year - 1

    # Initialize annual_bills_paid for this profile
    profile_annual_bills_paid = {}

    while current_date <= to_date:
        # Annual salary increase (2-4%) on the first day of each year
        if current_date.month == 1 and current_date.day == 1 and current_date.year > last_salary_increase_year:
            increase_rate = random.uniform(0.02, 0.04)  # 2-4% increase
            salary = round_to_cents(salary * (1 + increase_rate))
            if partner_salary > 0:
                partner_salary = round_to_cents(partner_salary * (1 + increase_rate))
            total_salary = salary + partner_salary
            last_salary_increase_year = current_date.year

            # Recalculate fixed expenses and available money
            adjusted_housing_range = adjust_range(consumption_profile["monthly"]["housing"][1 if profile_data['owns_house'] else 0]["range"], total_salary, index_fix)
            housing_expense = round_to_cents(random.uniform(*adjusted_housing_range))
            total_fixed_expenses = housing_expense
            for service in consumption_profile["monthly"]["basic_services"]:
                adjusted_range = adjust_range(service["range"], total_salary, index_fix)
                total_fixed_expenses += round_to_cents(random.uniform(*adjusted_range))
            for annual_bill in consumption_profile["annual"]:
                adjusted_range = adjust_range(annual_bill["range"], total_salary, index_fix)
                total_fixed_expenses += round_to_cents(random.uniform(*adjusted_range)) / 12
            available_money = total_salary - total_fixed_expenses

        # Monthly salary (or salaries)
        if current_date.day == 1:
            timestamp = generate_timestamp(current_date)
            trx_city = get_transaction_city(residence_city, nearby_cities, "incomes")
            balance += salary
            trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary", salary, balance))
            idx += 1

            if partner_salary > 0:
                trx_city = get_transaction_city(residence_city, nearby_cities, "incomes")
                balance += partner_salary
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_partner", partner_salary, balance))
                idx += 1

            # Extra income every 3-4 months
            months_since_last_extra_income += 1
            if months_since_last_extra_income >= random.randint(3, 4):
                trx_city = get_transaction_city(residence_city, nearby_cities, "incomes")
                balance += extra_income_amount
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "extra_income", extra_income_amount, balance))
                idx += 1
                months_since_last_extra_income = 0

            # Bonus in June and December
            if current_date.month in [6, 12]:
                trx_city = get_transaction_city(residence_city, nearby_cities, "incomes")
                bonus = round_to_cents(random.uniform(0.7 * salary, 0.8 * salary))
                balance += bonus
                trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_bonus", bonus, balance))
                idx += 1

                if partner_salary > 0:
                    trx_city = get_transaction_city(residence_city, nearby_cities, "incomes")
                    bonus_partner = round_to_cents(random.uniform(0.7 * partner_salary, 0.8 * partner_salary))
                    balance += bonus_partner
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "incomes", "salary_partner_bonus", bonus_partner, balance))
                    idx += 1

        # Rent or Mortgage (5th of each month)
        if current_date.day == 5:
            timestamp = generate_timestamp(current_date)
            trx_city = get_transaction_city(residence_city, nearby_cities, "expenses")

            balance -= housing_expense
            trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", "mortgage" if profile_data['owns_house'] else "rent", -housing_expense, balance))
            idx += 1

        # Annual bills (taxes and insurance in June or July)
        if current_date.month in [6, 7]:
            year_key = current_date.year
            if year_key not in profile_annual_bills_paid:
                profile_annual_bills_paid[year_key] = False

            if not profile_annual_bills_paid[year_key]:
                # 50% chance to bill in June, otherwise it will be billed in July
                if current_date.month == 7 or (current_date.month == 6 and random.random() < 0.5):
                    for annual_bill in consumption_profile["annual"]:
                        timestamp = generate_timestamp(current_date)
                        trx_city = get_transaction_city(residence_city, nearby_cities, "expenses")
                        adjusted_range = adjust_range(annual_bill["range"], total_salary, index_fix)
                        bill_amount = round_to_cents(random.uniform(*adjusted_range))
                        balance -= bill_amount
                        trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", annual_bill["concept"], -bill_amount, balance))
                        idx += 1
                    
                    profile_annual_bills_paid[year_key] = True

        # Utility bills (randomly distributed between 5th and 8th of each month)
        if 5 <= current_date.day <= 8:
            for service in consumption_profile["monthly"]["basic_services"]:
                # 25% chance each day to bill this service
                if random.random() < 0.25:
                    timestamp = generate_timestamp(current_date)
                    trx_city = get_transaction_city(residence_city, nearby_cities, "expenses")
                    adjusted_range = adjust_range(service["range"], total_salary, index_fix)
                    bill_amount = round_to_cents(random.uniform(*adjusted_range))
                    balance -= bill_amount
                    trxs.append(generate_transaction(customer_name, account_name, trx_city, idx, timestamp, "expenses", service["concept"], -bill_amount, balance))
                    idx += 1

        # Variable expenses
        index_var = profile_data['index_var_expenses']
        max_var_expenses = available_money * index_var

        all_categories = consumption_profile["frequent"] + consumption_profile["occasional"]
        
        daily_var_expenses = 0
        for category in all_categories:
            if random.random() < category["frequency"]:
                timestamp = generate_timestamp(current_date)
                adjusted_range = (category['range'][0], min(category['range'][1], max_var_expenses - daily_var_expenses))
                trx_amount = round_to_cents(random.uniform(*adjusted_range))
                daily_var_expenses += trx_amount
                balance -= trx_amount
                trx_category = category['concept']
                trx_city = get_transaction_city(residence_city, nearby_cities, "expenses")
                trxs.append(generate_transaction(
                    customer_name, 
                    account_name,
                    trx_city,
                    idx, 
                    timestamp, 
                    "expenses", 
                    trx_category, 
                    -trx_amount, 
                    balance
                ))
                idx += 1

                if daily_var_expenses >= max_var_expenses:
                    break

        # Conditional expenses
        for condition in consumption_profile["conditional"]:
            if condition["concept"] == "children" and profile_data["children"] > 0:
                if random.random() < condition["frequency"] and daily_var_expenses < max_var_expenses:
                    timestamp = generate_timestamp(current_date)
                    trx_city = get_transaction_city(residence_city, nearby_cities, "expenses")
                    adjusted_range = adjust_range(condition["range"], total_salary, index_var)
                    base_child_expense = round_to_cents(random.uniform(*adjusted_range))
                    child_expense = base_child_expense * profile_data["children"]
                    
                    # Increase by 30% for each additional child
                    if profile_data["children"] > 1:
                        child_expense *= (1 + (profile_data["children"] - 1) * 0.3)
                    
                    child_expense = min(round_to_cents(child_expense), max_var_expenses - daily_var_expenses)
                    balance -= child_expense
                    daily_var_expenses += child_expense
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
                if random.random() < condition["frequency"] and daily_var_expenses < max_var_expenses:
                    timestamp = generate_timestamp(current_date)
                    trx_city = get_transaction_city(residence_city, nearby_cities, "expenses")
                    adjusted_range = adjust_range(condition["range"], total_salary, index_var)
                    car_expense = min(round_to_cents(random.uniform(*adjusted_range)), max_var_expenses - daily_var_expenses)
                    balance -= car_expense
                    daily_var_expenses += car_expense
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
    }, profile_annual_bills_paid