import random
import pandas as pd
from user_state import generate_users
from transaction_engine import (
    generate_normal_transaction
)
from fraud_engine import (
    generate_low_value_fraud,
    generate_velocity_fraud,
    generate_gradual_draining_fraud,
    generate_behavior_cloning_fraud,
    generate_adaptive_fraud
)
from feature_builder import ( enrich_transaction)

users = generate_users(100)
transaction_stream = []
for step in range(10000):
    user = random.choice( list(users.values()) )
    fraud_probability = ( 0.005 + user["risk_score"] * 0.02)
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
            transaction = ( generate_adaptive_fraud(user) )
        elif fraud_choice == "velocity":
            transaction = ( generate_velocity_fraud(user) )
        elif fraud_choice == "gradual":
            transaction = ( generate_gradual_draining_fraud(user) )
        elif fraud_choice == "cloning":
            transaction = ( generate_behavior_cloning_fraud(user) )
        else:
            transaction = ( generate_low_value_fraud(user) )
        if isinstance(transaction, list):
            valid_transactions = []
            for txn in transaction:
                if txn is not None:
                    txn = enrich_transaction(txn,user)
                    valid_transactions.append(txn)
            if len(valid_transactions) > 0:
                transaction_stream.extend(valid_transactions)
        else:
            if transaction is not None:
                transaction = enrich_transaction(transaction,user)
                transaction_stream.append(transaction)
    else:
        transaction = (generate_normal_transaction(user))
        if transaction is not None:
            transaction = enrich_transaction(transaction,user)
            transaction_stream.append(transaction)
    recent_history = (user["transaction_history"][-20:])
    if len(recent_history) > 0:
        avg_spend = sum(txn["amount"]
            for txn in recent_history
        ) / len(recent_history)
        user["avg_transaction_amount"] = (avg_spend)

df = pd.DataFrame(transaction_stream)
df = df.sort_values(by="timestamp")
df = df.reset_index(drop=True)
df.to_csv("streaming_transactions.csv",index=False)

# ============================================
# QUICK VALIDATION
# ============================================

print("\nFIRST 5 TRANSACTIONS\n")

print(df.head())

print("\nFRAUD TYPE DISTRIBUTION\n")

print(
    df["fraud_type"]
    .value_counts()
)

print("\nFRAUD LABEL DISTRIBUTION\n")

print(
    df["fraud_label"]
    .value_counts()
)

print("\nMINIMUM BALANCE\n")

print(
    df["remaining_balance"].min()
)

print("\nFINAL COLUMNS\n")

print(df.columns)
print(df.columns.tolist())