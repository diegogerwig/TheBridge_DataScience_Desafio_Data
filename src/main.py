from transactions import generate_transactions
from datetime import datetime
import json
from pathlib import Path
from config import income_profiles
from utils import save_to_csv

if __name__ == "__main__":
    start_date = "2022-01-01"
    all_transactions = []
    
    for profile in income_profiles.keys():
        print(f"\nGenerating data for {profile} profile...")
        data = generate_transactions(profile, datetime.strptime(start_date, "%Y-%m-%d"))
        
        # Add profile information to each transaction
        for transaction in data['transactions']:
            transaction['profile'] = profile
        
        all_transactions.extend(data['transactions'])
        print(f"✅ Generated {data['transaction_count']} transactions for {profile}")

    # Create data folder
    data_folder = Path(__file__).parent.parent / "data"
    data_folder.mkdir(parents=True, exist_ok=True)
    
    # Use fixed filename
    fixed_filename = "data_bank_trx_2024_10_07_23_15"

    # Save all transactions to a single JSON file
    json_filename = f"{fixed_filename}.json"
    json_filepath = data_folder / json_filename
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_transactions, f, ensure_ascii=False, indent=2)
    
    # Save all transactions to a single CSV file using the utility function
    csv_filepath = save_to_csv(all_transactions, fixed_filename)

    # Print information about saved files
    json_relative_path = json_filepath.relative_to(Path(__file__).parent.parent)
    csv_relative_path = csv_filepath.relative_to(Path(__file__).parent.parent)

    print(f"\n✅ Total transactions generated: {len(all_transactions)}")
    print(f"✅ JSON file saved at: {json_relative_path}")
    print(f"✅ CSV  file saved at: {csv_relative_path}")

    print("\n🚀 Done generating data for all profiles!")