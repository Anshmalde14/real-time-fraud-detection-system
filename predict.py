import joblib
import pandas as pd


# ============================================
# LOAD TRAINED MODEL
# ============================================

model = joblib.load(
    "fraud_model.pkl"
)


# ============================================
# THRESHOLD
# ============================================

THRESHOLD = 0.60


# ============================================
# FEATURE ORDER
# MUST MATCH TRAINING
# ============================================

FEATURE_COLUMNS = [

    "transaction_gap_seconds",

    "transactions_last_5min",

    "device_change",

    "amount",

    "amount_balance_ratio",

    "transaction_hour",

    "user_type",

    "merchant_category",

    "merchant",

    "location",

    "device_type",

    "is_high_amount"
]


# ============================================
# PREDICTION FUNCTION
# ============================================

def predict_transaction(transaction_dict):

    input_df = pd.DataFrame(
        [transaction_dict]
    )

    input_df = input_df[
        FEATURE_COLUMNS
    ]

    fraud_probability = (

        model.predict_proba(
            input_df
        )[:,1][0]
    )

    fraud_prediction = int(

        fraud_probability >= THRESHOLD
    )

    return {

        "fraud_probability":
        float(round(fraud_probability, 4)),

        "fraud_prediction":
        fraud_prediction,

        "risk_level":
        get_risk_level(
            fraud_probability
        )
    }


# ============================================
# RISK LEVEL LOGIC
# ============================================

def get_risk_level(probability):

    if probability >= 0.85:

        return "HIGH"

    elif probability >= 0.60:

        return "MEDIUM"

    else:

        return "LOW"