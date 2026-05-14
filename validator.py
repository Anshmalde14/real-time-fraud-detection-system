import pandas as pd


df = pd.read_csv("synthetic_transactions.csv")


print("=" * 50)
print("DATASET SHAPE")
print("=" * 50)

print(df.shape)


print("\n" + "=" * 50)
print("FRAUD DISTRIBUTION")
print("=" * 50)

print(df["fraud_label"].value_counts())


print("\n" + "=" * 50)
print("FRAUD PERCENTAGE")
print("=" * 50)

fraud_percentage = (
    df["fraud_label"].mean() * 100
)

print(f"{fraud_percentage:.2f}%")


print("\n" + "=" * 50)
print("NEGATIVE BALANCES CHECK")
print("=" * 50)

negative_balances = df[df["new_balance"] < 0]

print("Negative balance rows:",
      len(negative_balances))


print("\n" + "=" * 50)
print("TRANSACTION AMOUNT STATS")
print("=" * 50)

print(df["amount"].describe())


print("\n" + "=" * 50)
print("FRAUD TYPES")
print("=" * 50)

print(df["fraud_type"].value_counts())


print("\n" + "=" * 50)
print("TOP MERCHANT CATEGORIES")
print("=" * 50)

print(df["merchant_category"].value_counts())


print("\n" + "=" * 50)
print("FOREIGN TRANSACTION COUNT")
print("=" * 50)

print(
    (df["is_foreign_transaction"] == 1).sum()
)


print("\n" + "=" * 50)
print("UNIQUE USERS")
print("=" * 50)

print(df["user_id"].nunique())


print("\n" + "=" * 50)
print("SAMPLE FRAUD TRANSACTIONS")
print("=" * 50)

frauds = df[df["fraud_label"] == 1]

print(
    frauds[[
        "user_id",
        "amount",
        "fraud_type",
        "location",
        "device_id"
    ]].head(10)
)