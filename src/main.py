import json
import csv
from datetime import datetime
from pathlib import Path
from config import buyer_profiles
from trx_generator import generate_trxs
from utils import generate_spanish_dni, generate_email, generate_password, save_json, save_csv, generate_final_report
import random

def generate_data(start_date):
    users = []
    transactions = []
    annual_bills_paid = {}

    print(f"\nGenerating data for {len(buyer_profiles)} profiles:")
    print("-" * 50)

    for profile_name, profile_data in buyer_profiles.items():
        dni = generate_spanish_dni()
        email = generate_email(profile_data['name'], profile_data['surname'])
        password = generate_password(6)

        initial_assets = round(float(random.uniform(*profile_data['initial_assets'])), 2)
        
        user = {
            "profile": profile_name,
            "name": profile_data['name'],
            "surname": profile_data['surname'],
            "birth_date": profile_data['birth_date'],
            "dni": dni,
            "email": email,
            "password": password,
            "city": profile_data['city'],
            "iban": profile_data['iban'],
            "assets": initial_assets,
        }
        users.append(user)
        
        data, annual_bills_paid = generate_trxs(profile_data, start_date, annual_bills_paid)
        
        for trx in data['trxs']:
            transaction = {
                "dni": dni,
                "type": "expenses" if trx['amount_eur'] < 0 else "incomes",
                "category": trx['trx_cat'],
                "amount": trx['amount_eur'],
                "timestamp": trx['timestamp']
            }
            transactions.append(transaction)
        
        print(f"💥 Total transactions for {user['profile']}: \t{len(data['trxs'])}")

    return users, transactions

if __name__ == "__main__":
    start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")

    users, transactions = generate_data(start_date)

    end_date = max(datetime.fromisoformat(t['timestamp']) for t in transactions)
    years_period = (end_date - start_date).days / 365

    # Create data folder outside of src
    project_root = Path(__file__).resolve().parent.parent
    data_folder = project_root / "data"
    data_folder.mkdir(exist_ok=True)

    # Save JSON files
    users_json_path = data_folder / "userInsert.json"
    transactions_json_path = data_folder / "transactionInsert.json"
    save_json(users, users_json_path)
    save_json(transactions, transactions_json_path)

    # Save CSV file
    csv_path = data_folder / "data_bank_trx.csv"
    save_csv(users, transactions, csv_path)

    # Generate final output
    try:
        users_json_relative_path = users_json_path.relative_to(project_root)
        transactions_json_relative_path = transactions_json_path.relative_to(project_root)
        csv_relative_path = csv_path.relative_to(project_root)
        
        print(f"\n✅ Total users generated: \t\t{len(users)}")
        print(f"✅ Total transactions generated: \t{len(transactions)}")
        print(f"✅ Users         JSON file saved at: \t{users_json_relative_path}")
        print(f"✅ Transactions  JSON file saved at: \t{transactions_json_relative_path}")
        print(f"✅ Data          CSV  file saved at: \t{csv_relative_path}")
    except ValueError as e:
        print(f"\n❌ Error calculating relative paths: {e}")
        print(f"✅ Total users generated: {len(users)}")
        print(f"✅ Total transactions generated: {len(transactions)}")
        print(f"✅ Users JSON file saved at: {users_json_path}")
        print(f"✅ Transactions JSON file saved at: {transactions_json_path}")
        print(f"✅ CSV file saved at: {csv_path}")

    print("\n🚀 Done generating data!")
    
    # Generate and display final report for all profiles
    final_report = generate_final_report(users, transactions)
    print(f"\nFinal Report for all profiles (Period: {years_period:.2f} years)")
    print(final_report)