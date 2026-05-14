import pandas as pd
import pandas as pd


df = pd.read_csv("synthetic_transaction.csv")

fraud_count = (df["fraud_label"] == 1).sum()

print("Fraud Transactions:", fraud_count)