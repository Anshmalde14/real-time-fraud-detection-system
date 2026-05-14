import random
import uuid

from generator.profiles import (
    PROFILE_CONFIGS,
    choose_profile
)

INDIAN_CITIES = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Kolkata"
]

DEVICE_TYPES = [
    "Android",
    "iPhone",
    "Web"
]


class User:

    def __init__(self, user_id, profile_type):
        profile_data = PROFILE_CONFIGS[profile_type]
        self.user_id = user_id
        self.profile_type = profile_type
        self.home_location = random.choice(INDIAN_CITIES)
        self.account_balance = round(
            random.uniform(
                *profile_data["balance_range"]
            ),
            2
        )
        self.avg_transaction_amount = round(
            random.uniform(
                *profile_data["avg_transaction_range"]
            ),
            2
        )
        self.daily_transaction_limit = random.randint(
            *profile_data["daily_transaction_limit"]
        )
        self.active_hours = profile_data["active_hours"]
        self.merchant_categories = profile_data[
            "merchant_categories"
        ]
        self.account_age_days = random.randint(30, 4000)
        self.device_type = random.choice(DEVICE_TYPES)
        self.known_devices = self.generate_devices()
        self.last_transaction_time = None
        self.daily_transaction_count = 0

    def generate_devices(self):

        device_count = random.randint(1, 3)

        devices = []

        for _ in range(device_count):

            device_id = f"DEV_{uuid.uuid4().hex[:8]}"

            devices.append(device_id)

        return devices

    def to_dict(self):

        return {
            "user_id": self.user_id,
            "profile_type": self.profile_type,
            "home_location": self.home_location,
            "account_balance": self.account_balance,
            "avg_transaction_amount": self.avg_transaction_amount,
            "daily_transaction_limit": self.daily_transaction_limit,
            "active_hours": self.active_hours,
            "merchant_categories": self.merchant_categories,
            "account_age_days": self.account_age_days,
            "device_type": self.device_type,
            "known_devices": self.known_devices
        }
def generate_users(number_of_users):
    users = []
    for i in range(number_of_users):
        profile_type = choose_profile()
        user = User(
            user_id=f"USER_{i+1:04}",
            profile_type=profile_type
        )
        users.append(user)
    return users