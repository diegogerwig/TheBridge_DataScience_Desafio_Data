from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from transactions import generate_transactions

app = FastAPI()

@app.get("/")
def read_root():
    return "Welcome to the Bank Transaction Generation API!"

@app.get("/transactions")
def gen_transactions(profile: str, from_date: str):
    try:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    data = generate_transactions(profile, from_date)
    return JSONResponse(content=data)
