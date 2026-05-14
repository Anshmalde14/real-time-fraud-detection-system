import random

PROFILE_CONFIGS = {
    "student": {
        "balance_range": (2000, 30000),
        "avg_transaction_range": (100, 2000),
        "daily_transaction_limit": (5, 20),
        "active_hours": (10, 1),
        "merchant_categories": [
            "FOOD",
            "SHOPPING",
            "RECHARGE",
            "ENTERTAINMENT"
        ]
    },

    "salaried": {
        "balance_range": (20000, 200000),
        "avg_transaction_range": (500, 10000),
        "daily_transaction_limit": (3, 15),
        "active_hours": (7, 23),
        "merchant_categories": [
            "BILLS",
            "SHOPPING",
            "TRAVEL",
            "FOOD"
        ]
    },

    "business": {
        "balance_range": (100000, 5000000),
        "avg_transaction_range": (10000, 100000),
        "daily_transaction_limit": (10, 50),
        "active_hours": (6, 20),
        "merchant_categories": [
            "VENDOR",
            "PAYROLL",
            "SERVICES",
            "TRANSFER"
        ]
    },

    "high_net_worth": {
        "balance_range": (1000000, 10000000),
        "avg_transaction_range": (5000, 500000),
        "daily_transaction_limit": (2, 20),
        "active_hours": (8, 1),
        "merchant_categories": [
            "LUXURY",
            "TRAVEL",
            "HOTELS",
            "SHOPPING"
        ]
    },

    "elderly": {
        "balance_range": (50000, 1000000),
        "avg_transaction_range": (100, 5000),
        "daily_transaction_limit": (1, 10),
        "active_hours": (7, 21),
        "merchant_categories": [
            "MEDICAL",
            "GROCERY",
            "BILLS"
        ]
    }
}


PROFILE_DISTRIBUTION = {
    "student": 0.30,
    "salaried": 0.40,
    "business": 0.10,
    "high_net_worth": 0.05,
    "elderly": 0.15
}


def choose_profile():
    profiles = list(PROFILE_DISTRIBUTION.keys())
    probabilities = list(PROFILE_DISTRIBUTION.values())

    return random.choices(
        profiles,
        weights=probabilities,
        k=1
    )[0]