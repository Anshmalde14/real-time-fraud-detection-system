from datetime import datetime


user_last_transaction = {}

user_recent_transactions = {}

user_known_devices = {}


def enrich_transaction(
    transaction,
    user
):

    user_id = transaction["user_id"]

    current_time = transaction["timestamp"]

    amount = transaction["amount"]

    balance = transaction["remaining_balance"]

    location = transaction["location"]

    device = transaction["device_id"]

    # ============================================
    # TRANSACTION HOUR
    # ============================================

    transaction["transaction_hour"] = (
        current_time.hour
    )

    # ============================================
    # NIGHT TRANSACTION
    # ============================================

    transaction["is_night_transaction"] = int(

        current_time.hour >= 0
        and
        current_time.hour <= 5
    )

    # ============================================
    # FOREIGN TRANSACTION
    # ============================================

    transaction["is_foreign_transaction"] = int(

        location not in
        user["trusted_locations"]
    )

    # ============================================
    # AMOUNT BALANCE RATIO
    # ============================================

    if balance > 0:

        transaction["amount_balance_ratio"] = (

            amount / balance
        )

    else:

        transaction["amount_balance_ratio"] = 0

    # ============================================
    # HIGH AMOUNT FLAG
    # ============================================

    transaction["is_high_amount"] = int(

        amount >

        user["avg_transaction_amount"] * 2
    )

    # ============================================
    # DEVICE CHANGE
    # ============================================

    if user_id not in user_known_devices:

        user_known_devices[user_id] = set()

    if device in user_known_devices[user_id]:

        transaction["device_change"] = 0

    else:

        transaction["device_change"] = 1

        user_known_devices[user_id].add(
            device
        )

    # ============================================
    # PREVIOUS TRANSACTION TIME
    # ============================================

    previous_time = user_last_transaction.get(
        user_id
    )

    transaction["previous_transaction_time"] = (
        previous_time
    )

    # ============================================
    # TRANSACTION GAP
    # ============================================

    if previous_time is not None:

        gap = (
            current_time - previous_time
        ).total_seconds()

        transaction["transaction_gap_seconds"] = (
            gap
        )

    else:

        transaction["transaction_gap_seconds"] = (
            999999
        )

    # ============================================
    # RAPID TRANSACTION
    # ============================================

    transaction["rapid_transaction"] = int(

        transaction[
            "transaction_gap_seconds"
        ] < 120
    )

    # ============================================
    # LAST TRANSACTION UPDATE
    # ============================================

    user_last_transaction[user_id] = (
        current_time
    )

    # ============================================
    # TRANSACTIONS LAST 5 MINUTES
    # ============================================

    if user_id not in user_recent_transactions:

        user_recent_transactions[user_id] = []

    recent_times = []

    for txn_time in user_recent_transactions[user_id]:

        if (

            current_time - txn_time

        ).total_seconds() <= 300:

            recent_times.append(txn_time)

    recent_times.append(current_time)

    user_recent_transactions[user_id] = (
        recent_times
    )

    transaction["transactions_last_5min"] = (
        len(recent_times)
    )

    return transaction