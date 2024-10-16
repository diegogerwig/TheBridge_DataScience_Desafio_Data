import json
from datetime import datetime, date
from collections import defaultdict
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def load_data(transactions_file, users_file, goals_file):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data', 'data_Full_Stack'))
    
    transactions_path = os.path.join(data_dir, 'transactionInsert.json')
    users_path = os.path.join(data_dir, 'userInsert.json')
    goals_path = os.path.join(data_dir, 'savingsGoals.json')
    
    print(f"Looking for files in: {data_dir}")
    print(f"Transactions file path: {transactions_path}")
    print(f"Users file path: {users_path}")
    print(f"Goals file path: {goals_path}")
    
    try:
        with open(transactions_path, 'r') as file:
            transactions = json.load(file)
        print("✅ Transactions file loaded successfully")
        
        with open(users_path, 'r') as file:
            users = json.load(file)
        print("✅ Users file loaded successfully")
        
        goals = {}
        if os.path.exists(goals_path):
            with open(goals_path, 'r') as file:
                goals = json.load(file)
            print("✅ Goals file loaded successfully")
        else:
            print(f"ℹ️ Note: savingsGoals.json not found at {goals_path}. Proceeding without savings goals.")
        
        return transactions, users, goals
    except FileNotFoundError as e:
        print(f"❌ Error: Unable to find a required file. {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in one of the files. {e}")
        raise
    except Exception as e:
        print(f"❌ An unexpected error occurred while loading files: {e}")
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

def calculate_expense_variability(expenses):
    variability = {}
    for category in set(cat for month in expenses.values() for cat in month):
        category_expenses = [expenses[month].get(category, 0) for month in sorted(expenses.keys())]
        variability[category] = np.std(category_expenses) / np.mean(category_expenses) if np.mean(category_expenses) > 0 else 0
    return variability

def recommend_expense_reduction(predicted_expenses, expense_variability, savings_shortfall):
    recommendations = []
    sorted_expenses = sorted(predicted_expenses.items(), key=lambda x: expense_variability[x[0]], reverse=True)
    
    remaining_shortfall = savings_shortfall
    for category, amount in sorted_expenses:
        if remaining_shortfall <= 0:
            break
        reduction = min(amount * 0.1, remaining_shortfall)  # Suggest reducing up to 10% of the category or the remaining shortfall
        if reduction > 0:
            recommendations.append({
                "category": category,
                "current_amount": round(amount, 2),
                "suggested_reduction": round(reduction, 2),
                "new_amount": round(amount - reduction, 2)
            })
            remaining_shortfall -= reduction
    
    return recommendations

def process_users(transactions, users, goals):
    predictions = {}
    goals_analysis = {}
    
    for user in users:
        dni = user['dni']
        income, expenses = analyze_transactions(transactions, dni)
        predicted_income, predicted_expenses = predict_next_month(income, expenses)
        
        total_expenses = sum(predicted_expenses.values())
        net_balance = predicted_income - total_expenses
        
        expense_variability = calculate_expense_variability(expenses)
        
        user_goals = goals.get(dni, [])
        goals_analysis[dni] = []
        
        for goal in user_goals:
            goal_amount = goal['amount']
            target_date = datetime.strptime(goal['target_date'], "%Y-%m-%d").date()
            months_left = (target_date.year - date.today().year) * 12 + target_date.month - date.today().month
            monthly_saving_needed = goal_amount / max(months_left, 1)  # Avoid division by zero
            is_goal_achievable = net_balance >= monthly_saving_needed
            
            goal_analysis = {
                "name": goal['name'],
                "amount": goal_amount,
                "target_date": goal['target_date'],
                "months_left": months_left,
                "monthly_saving_needed": round(monthly_saving_needed, 2),
                "is_achievable": is_goal_achievable,
                "recommendations": []
            }
            
            if not is_goal_achievable:
                savings_shortfall = monthly_saving_needed - net_balance
                goal_analysis["recommendations"] = recommend_expense_reduction(predicted_expenses, expense_variability, savings_shortfall)
            
            goals_analysis[dni].append(goal_analysis)
        
        predictions[dni] = {
            "predicted_income": round(predicted_income, 2),
            "predicted_expenses": {k: round(v, 2) for k, v in predicted_expenses.items()},
            "total_expenses": round(total_expenses, 2),
            "net_balance": round(net_balance, 2)
        }
    
    return predictions, goals_analysis

def save_prediction(file_path, prediction):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(prediction, file, indent=2, ensure_ascii=False)
        print(f"✅ File successfully saved: {file_path}")
    except Exception as e:
        print(f"❌ Error saving file {file_path}: {e}")

# Main execution
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data', 'data_Full_Stack'))
predictions_output_file = os.path.join(data_dir, 'predictionNextMonthInsert.json')
goals_output_file = os.path.join(data_dir, 'goalsAnalysis.json')

print(f"Script directory: {script_dir}")
print(f"Data directory: {data_dir}")

try:
    transactions, users, goals = load_data(None, None, None)
    predictions, goals_analysis = process_users(transactions, users, goals)
    
    save_prediction(predictions_output_file, predictions)
    
    if goals:
        save_prediction(goals_output_file, goals_analysis)
        print(f"✅ Goals analysis and recommendations saved in {goals_output_file}")
    else:
        print("ℹ️ No savings goals found. Goals analysis was not generated.")
    
    print(f"✅ Predictions saved in {predictions_output_file}")
    print(f"📁 Check the following directory for output files: {data_dir}")
except Exception as e:
    print(f"❌ An error occurred: {e}")