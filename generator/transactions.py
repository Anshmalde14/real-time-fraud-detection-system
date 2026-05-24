import random
import uuid
from generator.fraud_rules import apply_random_fraud
from datetime import datetime, timedelta

TRANSACTION_TYPES = [
    "UPI",
    "CARD",
    "BANK_TRANSFER",
    "WALLET",
    "ATM"
]

def generate_transaction_amount(user):
    base_amount = user.avg_transaction_amount
    variation = random.uniform(0.5, 1.5)
    amount = base_amount * variation
    return round(amount, 2)

def choose_merchant_category(user):
    return random.choice(user.merchant_categories)

def choose_transaction_type():
    return random.choice(TRANSACTION_TYPES)

def choose_device(user):
    return random.choice(user.known_devices)

def generate_transaction_time(user):
    start_hour, end_hour = user.active_hours
    current_time = datetime.now()
    if start_hour < end_hour:
        random_hour = random.randint(start_hour, end_hour)
    else:
        possible_hours = list(range(start_hour, 24)) + \
                         list(range(0, end_hour + 1))
        random_hour = random.choice(possible_hours)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    transaction_time = current_time.replace(
        hour=random_hour,
        minute=random_minute,
        second=random_second
    )
    return transaction_time

def update_user_balance(user, amount):
    old_balance = user.account_balance
    new_balance = old_balance - amount
    if new_balance < 0:
        new_balance = old_balance
    else:
        user.account_balance = new_balance
    return round(old_balance, 2), round(new_balance, 2)

def generate_transaction(user):
    amount = generate_transaction_amount(user)
    merchant_category = choose_merchant_category(user)
    transaction_type = choose_transaction_type()
    device_id = choose_device(user)
    timestamp = generate_transaction_time(user)
    old_balance, new_balance = update_user_balance(
        user,
        amount
    )
    transaction = {
        "transaction_id":
            f"TXN_{uuid.uuid4().hex[:10]}",
        "user_id":
            user.user_id,
        "timestamp":
            str(timestamp),
        "amount":
            amount,
        "merchant_category":
            merchant_category,
        "transaction_type":
            transaction_type,
        "location":
            user.home_location,
        "device_type":
            user.device_type,
        "device_id":
            device_id,
        "old_balance":
            old_balance,
        "new_balance":
            new_balance,
        "account_age_days":
            user.account_age_days,
        "daily_transaction_count":
            user.daily_transaction_count,
        "fraud_label":
            0
    }

    fraud_probability = 0.02

    if random.random() < fraud_probability:

        transaction = apply_random_fraud(
            transaction,
            user
        )
    user.daily_transaction_count += 1

    user.last_transaction_time = timestamp
    return transaction