import random
import uuid


# ============================================
# USER TYPES
# ============================================

USER_TYPES = [

    "student",

    "salaried",

    "business",

    "high_net_worth"
]


# ============================================
# INDIAN CITIES
# ============================================

INDIAN_CITIES = [

    "Mumbai",

    "Delhi",

    "Bangalore",

    "Hyderabad",

    "Chennai",

    "Pune",

    "Ahmedabad",

    "Kolkata"
]


# ============================================
# DEVICE TYPES
# ============================================

DEVICE_TYPES = [

    "android",

    "ios",

    "web"
]


# ============================================
# USER GENERATOR
# ============================================

def generate_users(num_users=100):

    users = {}

    for i in range(num_users):

        user_id = f"USER_{i:04d}"

        user_type = random.choice(
            USER_TYPES
        )

        # ============================================
        # BALANCE DISTRIBUTION
        # ============================================

        if user_type == "student":

            balance = round(

                random.uniform(
                    1000,
                    20000
                ),

                2
            )

            avg_transaction_amount = round(

                random.uniform(
                    100,
                    1500
                ),

                2
            )

        elif user_type == "salaried":

            balance = round(

                random.uniform(
                    20000,
                    150000
                ),

                2
            )

            avg_transaction_amount = round(

                random.uniform(
                    500,
                    5000
                ),

                2
            )

        elif user_type == "business":

            balance = round(

                random.uniform(
                    100000,
                    500000
                ),

                2
            )

            avg_transaction_amount = round(

                random.uniform(
                    2000,
                    20000
                ),

                2
            )

        else:

            balance = round(

                random.uniform(
                    500000,
                    5000000
                ),

                2
            )

            avg_transaction_amount = round(

                random.uniform(
                    5000,
                    50000
                ),

                2
            )

        # ============================================
        # TRUSTED LOCATIONS
        # ============================================

        trusted_locations = random.sample(

            INDIAN_CITIES,

            k=random.randint(1, 3)
        )

        # ============================================
        # TRUSTED DEVICES
        # ============================================

        trusted_devices = []

        for _ in range(
            random.randint(1, 3)
        ):

            trusted_devices.append(

                "DEVICE_" +

                str(uuid.uuid4())[:8]
            )

        # ============================================
        # USER OBJECT
        # ============================================

        users[user_id] = {

            "user_id":
            user_id,

            "user_type":
            user_type,

            "balance":
            balance,

            "account_age_days":
            random.randint(
                30,
                4000
            ),

            "avg_transaction_amount":
            avg_transaction_amount,

            "risk_score":
            round(
                random.uniform(0, 1),
                2
            ),

            "trusted_locations":
            trusted_locations,

            "trusted_devices":
            trusted_devices,

            "transaction_history":
            []
        }

    return users