from transactions import generate_transactions
from datetime import datetime
import json
from collections import OrderedDict
from pathlib import Path
from config import buyer_profiles
from utils import save_to_csv

def order_transaction(transaction, profile_name, profile_data):
    # Crear un diccionario ordenado con el orden de los campos correcto
    return OrderedDict([
        ('profile', profile_name),
        ('name', profile_data['name']),
        ('age', profile_data['age']),
        ('iban', profile_data['iban']),
        ('trx_id', transaction['trx_id']),
        ('timestamp', transaction['timestamp']),
        ('city', transaction['city']),
        ('transaction_type', transaction['transaction_type']),
        ('transaction_category', transaction['transaction_category']),
        ('amount_eur', transaction['amount_eur']),
        ('balance', transaction['balance'])
    ])

if __name__ == "__main__":
    start_date = "2020-01-01"
    all_transactions = []
    
    for profile_name, profile_data in buyer_profiles.items():
        print(f"\nGenerating data for {profile_name} profile...")
        data = generate_transactions(profile_data, datetime.strptime(start_date, "%Y-%m-%d"))
        
        for transaction in data['transactions']:
            ordered_transaction = order_transaction(transaction, profile_name, profile_data)
            all_transactions.append(ordered_transaction)
        
        print(f"✅ Generated {data['transaction_count']} transactions for {profile_name}")

    # Crear carpeta de datos
    project_root = Path(__file__).resolve().parent.parent
    data_folder = project_root / "data"
    data_folder.mkdir(parents=True, exist_ok=True)
    
    # Generar nombre de archivo con fecha y hora actuales
    current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M")
    filename = f"data_bank_trx_{current_datetime}"

    # Guardar todas las transacciones en un solo archivo JSON
    json_filename = f"{filename}.json"
    json_filepath = data_folder / json_filename
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(all_transactions, f, ensure_ascii=False, indent=2)
    
    # Guardar todas las transacciones en un archivo CSV utilizando la función utilitaria
    csv_filepath = save_to_csv(all_transactions, filename)

    # Imprimir información sobre los archivos guardados
    try:
        json_relative_path = json_filepath.relative_to(project_root)
        csv_relative_path = Path(csv_filepath).relative_to(project_root)
        
        print(f"\n✅ Total transactions generated: {len(all_transactions)}")
        print(f"✅ JSON file saved at: {json_relative_path}")
        print(f"✅ CSV  file saved at: {csv_relative_path}")
    except ValueError as e:
        print(f"\n❌ Error calculating relative paths: {e}")
        print(f"✅ Total transactions generated: {len(all_transactions)}")
        print(f"✅ JSON file saved at: {json_filepath}")
        print(f"✅ CSV  file saved at: {csv_filepath}")

    print("\n🚀 Done generating data for all profiles!")
