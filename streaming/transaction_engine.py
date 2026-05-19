import random
import uuid

from datetime import (
    datetime,
    timedelta
)


# ============================================
# GLOBAL DATA
# ============================================

MERCHANTS = {

    "grocery": [

        "DMart",
        "Reliance Fresh",
        "BigBasket"
    ],

    "electronics": [

        "Croma",
        "Vijay Sales",
        "Amazon"
    ],

    "restaurants": [

        "Dominos",
        "McDonalds",
        "KFC"
    ],

    "fashion": [

        "Zara",
        "H&M",
        "Lifestyle"
    ],

    "travel": [

        "Uber",
        "Ola",
        "MakeMyTrip"
    ]
}


FOREIGN_LOCATIONS = [

    "Dubai",
    "Singapore",
    "London",
    "Berlin",
    "Tokyo",
    "New York"
]


# ============================================
# TRANSACTION ID GENERATOR
# ============================================

def generate_transaction_id():

    return (

        "TXN_" +

        str(uuid.uuid4()).replace(
            "-",
            ""
        )[:10]
    )


# ============================================
# USER BEHAVIORAL HOURS
# ============================================

def generate_user_transaction_hour(user):

    user_type = user["user_type"]

    # ============================================
    # STUDENTS
    # MORE NIGHT ACTIVE
    # ============================================

    if user_type == "student":

        preferred_hours = [

            10,11,12,13,

            17,18,19,20,

            21,22,23
        ]

    # ============================================
    # BUSINESS USERS
    # EARLIER HOURS
    # ============================================

    elif user_type == "business":

        preferred_hours = [

            6,7,8,9,10,11,

            14,15,16,17,18
        ]

    # ============================================
    # HIGH NET WORTH
    # RANDOM FLEXIBLE HOURS
    # ============================================

    elif user_type == "high_net_worth":

        preferred_hours = list(
            range(24)
        )

    # ============================================
    # SALARIED USERS
    # EVENING HEAVY
    # ============================================

    else:

        preferred_hours = [

            7,8,9,

            18,19,20,21,22
        ]

    return random.choice(
        preferred_hours
    )


# ============================================
# NORMAL TRANSACTION GENERATOR
# ============================================

def generate_normal_transaction(user):

    old_balance = user["balance"]

    # ============================================
    # DYNAMIC USER SPENDING
    # ============================================

    avg_amount = user[
        "avg_transaction_amount"
    ]

    amount = round(

        random.uniform(

            avg_amount * 0.5,

            avg_amount * 1.5
        ),

        2
    )

    # ============================================
    # INSUFFICIENT BALANCE
    # ============================================

    if old_balance < amount:

        return None

    new_balance = round(

        old_balance - amount,

        2
    )

    # ============================================
    # CATEGORY + MERCHANT
    # ============================================

    category = random.choice(
        list(MERCHANTS.keys())
    )

    merchant = random.choice(
        MERCHANTS[category]
    )

    # ============================================
    # LOCATION BEHAVIOR
    # ============================================

    if user["user_type"] in [

        "business",

        "high_net_worth"
    ]:

        foreign_probability = 0.05

    else:

        foreign_probability = 0.01

    if random.random() < foreign_probability:

        location = random.choice(
            FOREIGN_LOCATIONS
        )

    else:

        location = random.choice(
            user["trusted_locations"]
        )

    # ============================================
    # DEVICE TYPE
    # ============================================

    device_type = random.choice([

        "android",

        "ios",

        "web"
    ])

    # ============================================
    # MOSTLY TRUSTED DEVICE
    # ============================================

    if random.random() < 0.75:

        device_id = random.choice(
            user["trusted_devices"]
        )

    else:

        device_id = (

            "DEVICE_" +

            str(uuid.uuid4())[:8]
        )

    # ============================================
    # REALISTIC TEMPORAL BEHAVIOR
    # ============================================

    current_time = datetime.now()

    transaction_hour = (
        generate_user_transaction_hour(
            user
        )
    )

    current_time = current_time.replace(

        hour=transaction_hour,

        minute=random.randint(0, 59),

        second=random.randint(0, 59)
    )

    # ============================================
    # SEQUENTIAL TIME EVOLUTION
    # ============================================

       # ============================================
# SEQUENTIAL TIME EVOLUTION
# ============================================

    if len(user["transaction_history"]) > 0:

        previous_time = user[
            "transaction_history"
        ][-1]["timestamp"]

        # ============================================
        # NORMAL HUMAN BURSTS
        # ============================================

        if random.random() < 0.30:

            gap_minutes = random.randint(
                1,
                8
            )

        # ============================================
        # NORMAL REGULAR ACTIVITY
        # ============================================

        else:

            gap_minutes = random.randint(
                10,
                300
            )

        current_time = previous_time + timedelta(
            minutes=gap_minutes
        )

    # ============================================
    # DAILY TRANSACTION COUNT
    # ============================================

    daily_transaction_count = random.randint(
        1,
        12
    )

    # ============================================
    # CREATE TRANSACTION
    # ============================================

    transaction = {

        "transaction_id":
        generate_transaction_id(),

        "user_id":
        user["user_id"],

        "user_type":
        user["user_type"],

        "amount":
        amount,

        "merchant_category":
        category,

        "merchant":
        merchant,

        "location":
        location,

        "device_type":
        device_type,

        "device_id":
        device_id,

        "timestamp":
        current_time,

        "old_balance":
        old_balance,

        "new_balance":
        new_balance,

        "remaining_balance":
        new_balance,

        "account_age_days":
        user["account_age_days"],

        "daily_transaction_count":
        daily_transaction_count,

        "fraud_label":
        0,

        "fraud_type":
        "normal"
    }

    # ============================================
    # UPDATE USER STATE
    # ============================================

    user["balance"] = new_balance

    user["transaction_history"].append(
        transaction
    )

    return transaction