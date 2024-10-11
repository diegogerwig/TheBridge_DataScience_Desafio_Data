from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from trx_generator import generate_trxs
from config import buyer_profiles
import uvicorn
from utils import generate_spanish_dni, generate_email, generate_password
import random
import bcrypt

app = FastAPI()

def encrypt_value(value):
    return bcrypt.hashpw(str(value).encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

def generate_user_data(profile_name, profile_data):
    dni = generate_spanish_dni()
    email = generate_email(profile_data['name'], profile_data['surname'])
    password = generate_password(6)
    initial_assets = round(float(random.uniform(*profile_data['initial_assets'])), 2)

    return {
        "profile": encrypt_value(profile_name),
        "name": encrypt_value(profile_data['name']),
        "surname": encrypt_value(profile_data['surname']),
        "birth_date": encrypt_value(profile_data['birth_date']),
        "dni": encrypt_value(dni),
        "email": encrypt_value(email),
        "password": encrypt_value(password),
        "city": encrypt_value(profile_data['city']),
        "iban": encrypt_value(profile_data['iban']),
        "assets": encrypt_value(initial_assets),
    }

def generate_transaction_data(user, trxs):
    return [
        {
            "dni": encrypt_value(user["dni"]),
            "type": encrypt_value("expenses" if trx['amount_eur'] < 0 else "incomes"),
            "category": encrypt_value(trx['trx_cat']),
            "amount": encrypt_value(trx['amount_eur']),
            "timestamp": encrypt_value(trx['timestamp'])
        }
        for trx in trxs
    ]

@app.get("/")
def read_root():
    return "Welcome to the Bank Transaction Generation API!"

@app.get("/users")
def gen_users(
    profile: str = Query(None, description="Income profile: 'buyer_1', 'buyer_2', ..., 'buyer_8'. Leave empty for all profiles.")
):
    """
    Generate user data based on the specified profile(s).

    - **profile**: Select a buyer profile ('buyer_1', 'buyer_2', ..., 'buyer_8'). Leave empty to generate for all profiles.
    """
    if profile is not None and profile not in buyer_profiles:
        raise HTTPException(status_code=400, detail="Invalid profile. Choose from 'buyer_1', 'buyer_2', ..., 'buyer_8' or leave empty for all profiles.")

    users = []
    profiles_to_process = [profile] if profile else buyer_profiles.keys()

    for current_profile in profiles_to_process:
        profile_data = buyer_profiles[current_profile]
        user = generate_user_data(current_profile, profile_data)
        users.append(user)

    return JSONResponse(content=users)

@app.get("/transactions")
def gen_transactions(
    profile: str = Query(None, description="Income profile: 'buyer_1', 'buyer_2', ..., 'buyer_8'. Leave empty for all profiles."),
    from_date: str = Query(..., description="Start date in the format YYYY-MM-DD")
):
    """
    Generate transaction data based on the user's profile(s) and date.

    - **profile**: Select a buyer profile ('buyer_1', 'buyer_2', ..., 'buyer_8'). Leave empty to generate for all profiles.
    - **from_date**: Start date for generating transactions in `YYYY-MM-DD` format.
    """
    try:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if profile is not None and profile not in buyer_profiles:
        raise HTTPException(status_code=400, detail="Invalid profile. Choose from 'buyer_1', 'buyer_2', ..., 'buyer_8' or leave empty for all profiles.")

    transactions = []
    annual_bills_paid = {}

    profiles_to_process = [profile] if profile else buyer_profiles.keys()

    for current_profile in profiles_to_process:
        profile_data = buyer_profiles[current_profile]
        user = generate_user_data(current_profile, profile_data)
        trx_data, annual_bills_paid = generate_trxs(profile_data, from_date, annual_bills_paid)
        user_transactions = generate_transaction_data(user, trx_data['trxs'])
        transactions.extend(user_transactions)

    return JSONResponse(content=transactions)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)