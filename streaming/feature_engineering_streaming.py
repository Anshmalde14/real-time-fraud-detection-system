import pandas as pd

df = pd.read_csv(
    "streaming_transactions.csv"
)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values(by=["user_id", "timestamp"])
df = df.set_index("timestamp")
df["txns_last_5min"] = (df.groupby("user_id")["amount"].rolling("5min").count().reset_index(level=0, drop=True))
df["user_avg_amount"] = (df.groupby("user_id")["amount"].transform("mean"))
df["amount_vs_user_avg"] = (df["amount"] /df["user_avg_amount"])
df["seconds_since_last_txn"] = (df.groupby("user_id").apply(lambda group:group.index.to_series().diff().dt.total_seconds()).reset_index(level=0, drop=True))
df["seconds_since_last_txn"] = (df["seconds_since_last_txn"].fillna(999999))
seen_devices = {}

new_device_flags = []

for idx, row in df.iterrows():
    user = row["user_id"]
    device = row["device_id"]
    if user not in seen_devices:
        seen_devices[user] = set()
    if device in seen_devices[user]:
        new_device_flags.append(0)
    else:
        new_device_flags.append(1)
        seen_devices[user].add(device)

df["is_new_device"] = (new_device_flags)
df["previous_balance"] = (df.groupby("user_id")["remaining_balance"].shift(1))
df["balance_drain_percent"] = ((df["previous_balance"] - df["remaining_balance"]) / df["previous_balance"])
df["balance_drain_percent"] = (df["balance_drain_percent"].fillna(0))
df = df.reset_index()
df.to_csv("streaming_features.csv",index=False)
print(df.head())
print()
print(df.columns)