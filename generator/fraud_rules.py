import random
import uuid


FOREIGN_LOCATIONS = [
    "London",
    "New York",
    "Dubai",
    "Singapore",
    "Tokyo"
]


def inject_account_drain(transaction, user):

    large_amount = round(
        user.account_balance * random.uniform(0.7, 0.95),
        2
    )

    transaction["amount"] = large_amount

    transaction["old_balance"] = user.account_balance

    transaction["new_balance"] = round(
        user.account_balance - large_amount,
        2
    )

    user.account_balance = transaction["new_balance"]

    transaction["fraud_type"] = "ACCOUNT_DRAIN"

    return transaction


def inject_velocity_fraud(transaction, user):

    transaction["time_since_last_transaction"] = random.randint(1, 10)

    transaction["daily_transaction_count"] += random.randint(10, 30)

    transaction["fraud_type"] = "VELOCITY_FRAUD"

    return transaction


def inject_device_fraud(transaction, user):

    new_device = f"DEV_{uuid.uuid4().hex[:8]}"

    transaction["device_id"] = new_device

    transaction["device_type"] = random.choice(
        ["Android", "iPhone", "Web"]
    )

    transaction["fraud_type"] = "DEVICE_TAKEOVER"

    return transaction


def inject_location_fraud(transaction, user):

    foreign_location = random.choice(
        FOREIGN_LOCATIONS
    )

    transaction["location"] = foreign_location

    transaction["is_foreign_transaction"] = 1

    transaction["fraud_type"] = "IMPOSSIBLE_TRAVEL"

    return transaction


def inject_card_testing_fraud(transaction, user):

    transaction["amount"] = round(
        random.uniform(1, 20),
        2
    )

    transaction["merchant_category"] = random.choice(
        ["SHOPPING", "CRYPTO", "GAMING"]
    )

    transaction["fraud_type"] = "CARD_TESTING"

    return transaction


def apply_random_fraud(transaction, user):

    fraud_functions = [

        inject_account_drain,

        inject_velocity_fraud,

        inject_device_fraud,

        inject_location_fraud,

        inject_card_testing_fraud
    ]

    chosen_fraud = random.choice(fraud_functions)

    transaction = chosen_fraud(transaction, user)

    transaction["fraud_label"] = 1

    return transaction