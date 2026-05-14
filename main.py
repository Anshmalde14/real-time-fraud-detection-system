import pandas as pd

from generator.users import generate_users
from generator.transactions import generate_transaction


users = generate_users(100)

transactions = []

for _ in range(10000):

    user = users[_ % len(users)]

    transaction = generate_transaction(user)

    transactions.append(transaction)


df = pd.DataFrame(transactions)

print(df.head())

print("\nFraud Distribution:")
print(df["fraud_label"].value_counts())

df.to_csv(
    "synthetic_transaction.csv",
    index=False
)

print("\nDataset Generated Successfully.")