from transactions import generate_transactions
from datetime import datetime
import json
from pathlib import Path

if __name__ == "__main__":
    start_date = "2022-01-01"
    profile = "High income"
    data = generate_transactions(profile, datetime.strptime(start_date, "%Y-%m-%d"))

    for transaction in data['transactions']:
        print(json.dumps(transaction, indent=2))

    json_folder = Path(__file__).parent.parent / "data"
    json_folder.mkdir(parents=True, exist_ok=True)
    
    json_filename = f"data_bank_trx_{datetime.now().strftime('%Y_%m_%d__%H_%M')}.json"
    json_filepath = json_folder / json_filename
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(data['transactions'], f, ensure_ascii=False, indent=2)
    
    csv_full_path = Path(data['csv_path'])
    csv_filename = csv_full_path.name  # Solo el nombre del archivo con extensión
    csv_dir = csv_full_path.parent.name  # Solo el nombre del directorio

    json_relative_path = json_filepath.relative_to(Path(__file__).parent.parent)

    print(f"✅ Generated {data['transaction_count']} transactions")
    print(f"✅ CSV  file saved at: {csv_dir}/{csv_filename}")
    print(f"✅ JSON file saved at: {json_relative_path}")

    print("\n🚀 Done!")
