import time
import pandas as pd
import random
import requests

from streaming.user_state import (
    generate_users
)

from streaming.transaction_engine import (
    generate_normal_transaction
)

from streaming.fraud_engine import (

    generate_low_value_fraud,

    generate_velocity_fraud,

    generate_gradual_draining_fraud,

    generate_behavior_cloning_fraud,

    generate_adaptive_fraud
)


# ============================================
# CREATE USERS
# ============================================

users = generate_users(100)


# ============================================
# LIVE STREAM LOOP
# ============================================

while True:

    user = random.choice(
        list(users.values())
    )

    fraud_probability = (

        0.005 +

        user["risk_score"] * 0.02
    )

    # ============================================
    # FRAUD OR NORMAL
    # ============================================

    if random.random() < fraud_probability:

        fraud_choice = random.choices(

            population=[

                "low_value",

                "velocity",

                "cloning",

                "gradual",

                "adaptive"
            ],

            weights=[

                40,
                25,
                20,
                10,
                5
            ],

            k=1
        )[0]

        if fraud_choice == "adaptive":

            transaction = (
                generate_adaptive_fraud(user)
            )

        elif fraud_choice == "velocity":

            transaction = (
                generate_velocity_fraud(user)
            )

        elif fraud_choice == "gradual":

            transaction = (
                generate_gradual_draining_fraud(user)
            )

        elif fraud_choice == "cloning":

            transaction = (
                generate_behavior_cloning_fraud(user)
            )

        else:

            transaction = (
                generate_low_value_fraud(user)
            )

    else:

        transaction = (
            generate_normal_transaction(user)
        )

    # ============================================
    # HANDLE MULTIPLE TRANSACTIONS
    # ============================================

    if isinstance(transaction, list):

        transactions = transaction

    else:

        transactions = [transaction]

    # ============================================
    # PROCESS EACH TRANSACTION
    # ============================================

    for txn in transactions:

        if txn is None:

            continue

        # ============================================
        # FEATURE ENGINEERING
        # ============================================

        txn["transaction_gap_seconds"] = random.randint(
            1,
            1000
        )

        txn["transactions_last_5min"] = random.randint(
            0,
            10
        )

        txn["device_change"] = random.randint(
            0,
            1
        )

        txn["amount_balance_ratio"] = round(

            txn["amount"] /

            max(txn["remaining_balance"], 1),

            4
        )

        txn["transaction_hour"] = txn[
            "timestamp"
        ].hour

        txn["is_high_amount"] = int(
            txn["amount"] > 5000
        )

        # ============================================
        # TEMPORARY ENCODINGS
        # ============================================

        txn["user_type_encoded"] = random.randint(
            0,
            3
        )

        txn["merchant_category_encoded"] = random.randint(
            0,
            4
        )

        txn["merchant_encoded"] = random.randint(
            0,
            14
        )

        txn["location_encoded"] = random.randint(
            0,
            10
        )

        txn["device_type_encoded"] = random.randint(
            0,
            2
        )

        # ============================================
        # API INPUT
        # ============================================

        api_input = {

            "transaction_gap_seconds":
            txn["transaction_gap_seconds"],

            "transactions_last_5min":
            txn["transactions_last_5min"],

            "device_change":
            txn["device_change"],

            "amount":
            txn["amount"],

            "amount_balance_ratio":
            txn["amount_balance_ratio"],

            "transaction_hour":
            txn["transaction_hour"],

            "user_type":
            txn["user_type_encoded"],

            "merchant_category":
            txn["merchant_category_encoded"],

            "merchant":
            txn["merchant_encoded"],

            "location":
            txn["location_encoded"],

            "device_type":
            txn["device_type_encoded"],

            "is_high_amount":
            txn["is_high_amount"]
        }

        # ============================================
        # SEND TO FASTAPI
        # ============================================

        try:

            response = requests.post(

                "http://127.0.0.1:8000/predict",

                json=api_input
            )

            prediction = response.json()
            
            # ============================================
# STORE LIVE RESULT
# ============================================

            txn["fraud_probability"] = (
                prediction["fraud_probability"]
            )

            txn["risk_level"] = (
                prediction["risk_level"]
            )

            txn["prediction"] = (
                prediction["fraud_prediction"]
            )

            import pandas as pd

            live_df = pd.DataFrame([txn])

            live_df.to_csv(

                "live_transactions.csv",

                mode="a",

                header=not pd.io.common.file_exists(
                    "live_transactions.csv"
                ),

                index=False
            )

            print()

            print("=" * 60)

            print("LIVE TRANSACTION")

            print("=" * 60)

            print(
                f"User ID: {txn['user_id']}"
            )

            print(
                f"Amount: {txn['amount']}"
            )

            print(
                f"Merchant: {txn['merchant']}"
            )

            print(
                f"Location: {txn['location']}"
            )

            print(
                f"Fraud Probability: "
                f"{prediction['fraud_probability']}"
            )

            print(
                f"Risk Level: "
                f"{prediction['risk_level']}"
            )

            print(
                f"Prediction: "
                f"{prediction['fraud_prediction']}"
            )

            print("=" * 60)

        except Exception as e:

            print(
                "API ERROR:",
                e
            )

    # ============================================
    # STREAM SPEED
    # ============================================

    time.sleep(1)