from fastapi import FastAPI
from predict import (
    predict_transaction
)
from pydantic import BaseModel

app = FastAPI()

class TransactionInput(BaseModel):
    transaction_gap_seconds: float
    transactions_last_5min: int
    device_change: int
    amount: float
    amount_balance_ratio: float
    transaction_hour: int
    user_type: int
    merchant_category: int
    merchant: int
    location: int
    device_type: int
    is_high_amount: int

@app.get("/")
def home():
    return {

        "message":
        "Fraud Detection API Running"
    }

@app.post("/predict")
def predict(data: TransactionInput):
    transaction_dict = data.dict()
    prediction = predict_transaction(transaction_dict )
    return prediction