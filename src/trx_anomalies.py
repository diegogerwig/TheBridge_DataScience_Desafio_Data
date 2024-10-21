import json
from datetime import datetime, timedelta
from collections import defaultdict
import os
import numpy as np

ANOMALY_MARGIN = 0.30  

def load_data(transactions_file, users_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    transactions_path = os.path.join(script_dir, '..', 'data', 'data_Full_Stack', 'transactionInsert.json')
    users_path = os.path.join(script_dir, '..', 'data', 'data_Full_Stack', 'userInsert.json')
    
    try:
        with open(transactions_path, 'r') as file:
            transactions = json.load(file)
        with open(users_path, 'r') as file:
            users = json.load(file)
        return transactions, users
    except FileNotFoundError as e:
        print(f"Error: Unable to find the file. {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script directory: {script_dir}")
        print(f"Attempted transactions path: {transactions_path}")
        print(f"Attempted users path: {users_path}")
        raise

def analyze_transactions(transactions, dni):
    income = defaultdict(float)
    expenses = defaultdict(lambda: defaultdict(float))
    all_transactions = []
    
    for transaction in transactions:
        if transaction['dni'] == dni:
            date = datetime.strptime(transaction['timestamp'], "%Y-%m-%dT%H:%M:%S")
            month_key = date.strftime("%Y-%m")
            
            if transaction['type'] == 'incomes':
                income[month_key] += transaction['amount']
            elif transaction['type'] == 'expenses':
                expenses[month_key][transaction['category']] += abs(transaction['amount'])
            
            all_transactions.append({
                'date': date,
                'type': transaction['type'],
                'category': transaction.get('category'),
                'amount': transaction['amount']
            })
    
    return income, expenses, all_transactions

def detect_anomalies(transactions, margin=ANOMALY_MARGIN):
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)
    
    # Separate recent and historical transactions
    recent_transactions = [t for t in transactions if t['date'] > thirty_days_ago]
    historical_transactions = [t for t in transactions if t['date'] <= thirty_days_ago]
    
    anomalies = []
    
    # Calculate historical averages
    historical_averages = defaultdict(lambda: defaultdict(list))
    for t in historical_transactions:
        historical_averages[t['type']][t['category']].append(abs(t['amount']))
    
    for category in historical_averages['expenses']:
        historical_averages['expenses'][category] = np.mean(historical_averages['expenses'][category])
    
    if historical_averages['incomes']:
        historical_averages['incomes'] = np.mean(historical_averages['incomes']['salary'])
    
    # Check recent transactions for anomalies
    for t in recent_transactions:
        if t['type'] == 'expenses':
            avg = historical_averages['expenses'].get(t['category'], 0)
            if abs(t['amount']) > avg * (1 + margin):
                anomalies.append({
                    'date': t['date'].strftime("%Y-%m-%d"),
                    'type': t['type'],
                    'category': t['category'],
                    'amount': abs(t['amount']),
                    'average': avg,
                    'difference_percentage': ((abs(t['amount']) - avg) / avg) * 100 if avg > 0 else 100
                })
        elif t['type'] == 'incomes':
            avg = historical_averages['incomes']
            if t['amount'] > avg * (1 + margin):
                anomalies.append({
                    'date': t['date'].strftime("%Y-%m-%d"),
                    'type': t['type'],
                    'category': t['category'],
                    'amount': t['amount'],
                    'average': avg,
                    'difference_percentage': ((t['amount'] - avg) / avg) * 100 if avg > 0 else 100
                })
    
    return anomalies

def process_users(transactions, users):
    predictions = {}
    for user in users:
        dni = user['dni']
        income, expenses, all_transactions = analyze_transactions(transactions, dni)
        anomalies = detect_anomalies(all_transactions)
        
        predictions[dni] = {
            "anomalies": anomalies
        }
    
    return predictions

def save_prediction(file_path, prediction):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(prediction, file, indent=2, ensure_ascii=False)

# Main execution
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, '../data/data_Full_Stack/transactionAnomaliesInsert.json')

try:
    transactions, users = load_data(None, None)
    predictions = process_users(transactions, users)
    save_prediction(output_file, predictions)
    print(f"✅ Anomalies saved in {output_file}")
except Exception as e:
    print(f"❌ An error occurred: {e}")