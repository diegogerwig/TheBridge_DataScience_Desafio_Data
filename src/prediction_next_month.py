import json
from datetime import datetime, timedelta
from collections import defaultdict
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

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
    
    for transaction in transactions:
        if transaction['dni'] == dni:
            date = datetime.strptime(transaction['timestamp'], "%Y-%m-%dT%H:%M:%S")
            month_key = date.strftime("%Y-%m")
            
            if transaction['type'] == 'incomes':
                income[month_key] += transaction['amount']
            elif transaction['type'] == 'expenses':
                expenses[month_key][transaction['category']] += abs(transaction['amount'])
    
    return income, expenses

def predict_next_month(income, expenses):
    def train_model(data):
        X = np.array(range(len(data))).reshape(-1, 1)
        y = np.array(data)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = LinearRegression()
        model.fit(X_scaled, y)
        next_month = scaler.transform([[len(data)]])
        prediction = model.predict(next_month)
        return max(0, prediction[0])  # Ensure non-negative prediction

    # Predict income
    income_values = list(income.values())
    predicted_income = train_model(income_values) if len(income_values) > 1 else (income_values[0] if income_values else 0)

    # Predict expenses
    predicted_expenses = {}
    for category in set(cat for month in expenses.values() for cat in month):
        category_expenses = [expenses[month].get(category, 0) for month in sorted(expenses.keys())]
        predicted_expenses[category] = train_model(category_expenses) if len(category_expenses) > 1 else (category_expenses[0] if category_expenses else 0)

    return predicted_income, predicted_expenses

def process_users(transactions, users):
    predictions = {}
    for user in users:
        dni = user['dni']
        income, expenses = analyze_transactions(transactions, dni)
        predicted_income, predicted_expenses = predict_next_month(income, expenses)
        
        predictions[dni] = {
            "predicted_income": round(predicted_income, 2),
            "predicted_expenses": {k: round(v, 2) for k, v in predicted_expenses.items()},
            "net_balance": round(predicted_income - sum(predicted_expenses.values()), 2)
        }
    
    return predictions

def save_prediction(file_path, prediction):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(prediction, file, indent=2, ensure_ascii=False)

# Main execution
script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, '../data/data_Full_Stack/predictionNextMonthInsert.json')

try:
    transactions, users = load_data(None, None)
    predictions = process_users(transactions, users)
    save_prediction(output_file, predictions)
    print(f"✅ Predictions saved in {output_file}")
except Exception as e:
    print(f"❌ An error occurred: {e}")