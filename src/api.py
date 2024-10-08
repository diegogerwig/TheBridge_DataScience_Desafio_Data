from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from trx_generator import generate_trxs
from config import buyer_profiles

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the Bank Transaction Generation API!"

@app.get("/transactions")
def gen_transactions(
    profile: str = Query(..., description="Income profile: 'buyer_1', 'buyer_2', 'buyer_3', etc."), 
    from_date: str = Query(..., description="Start date in the format YYYY-MM-DD")
):
    """
    Generate bank transactions based on the user's profile and date.

    - **profile**: Select a buyer profile ('buyer_1', 'buyer_2', 'buyer_3', etc.).
    - **from_date**: Start date for generating transactions in `YYYY-MM-DD` format.
    """
    try:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    if profile not in buyer_profiles:
        raise HTTPException(status_code=400, detail="Invalid profile. Choose from 'buyer_1', 'buyer_2', 'buyer_3', etc.")

    profile_data = buyer_profiles[profile]
    data = generate_trxs(profile_data, from_date)
    return JSONResponse(content=data)