import random
import uuid

from datetime import (
    datetime,
    timedelta
)

from transaction_engine import (
    generate_transaction_id
)


# ============================================
# GLOBAL DATA
# ============================================

FOREIGN_LOCATIONS = [

    "Dubai",
    "Singapore",
    "London",
    "New York",
    "Berlin",
    "Tokyo"
]


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

        "MakeMyTrip",
        "Uber",
        "Ola"
    ]
}


# ============================================
# FRAUD TIME GENERATOR
# SLIGHT NIGHT BIAS ONLY
# ============================================

def generate_fraud_hour():

    fraud_hour = random.choices(

        population=list(range(24)),

        weights=[

            2 if h in [0,1,2,3,4]

            else 1

            for h in range(24)
        ],

        k=1
    )[0]

    return fraud_hour


# ============================================
# LOW VALUE FRAUD
# ============================================

def generate_low_value_fraud(user):

    amount = round(

        random.uniform(50, 500),

        2
    )

    old_balance = user["balance"]

    if old_balance < amount:

        return None

    new_balance = round(

        old_balance - amount,

        2
    )

    category = random.choice(
        list(MERCHANTS.keys())
    )

    merchant = random.choice(
        MERCHANTS[category]
    )

    # ============================================
    # FOREIGN BIAS FIX
    # ============================================

    if random.random() < 0.05:

        location = random.choice(
            FOREIGN_LOCATIONS
        )

    else:

        location = random.choice(
            user["trusted_locations"]
        )

    timestamp = datetime.now()

    fraud_hour = generate_fraud_hour()

    timestamp = timestamp.replace(
        hour=fraud_hour
    )

    device_type = random.choice([

        "android",
        "ios",
        "web"
    ])

    device_id = (
        "DEVICE_" +
        str(uuid.uuid4())[:8]
    )

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
        timestamp,

        "remaining_balance":
        new_balance,

        "fraud_label":
        1,

        "fraud_type":
        "low_value_fraud"
    }

    user["balance"] = new_balance

    user["transaction_history"].append(
        transaction
    )

    return transaction


# ============================================
# VELOCITY FRAUD
# ============================================

def generate_velocity_fraud(user):

    transactions = []

    num_transactions = random.randint(3, 6)

    base_time = datetime.now()

    # ============================================
    # FOREIGN BIAS FIX
    # ============================================

    if random.random() < 0.10:

        location = random.choice(
            FOREIGN_LOCATIONS
        )

    else:

        location = random.choice(
            user["trusted_locations"]
        )

    for i in range(num_transactions):

        amount = round(

            random.uniform(100, 1500),

            2
        )

        old_balance = user["balance"]

        if old_balance < amount:

            continue

        new_balance = round(

            old_balance - amount,

            2
        )

        category = random.choice(
            list(MERCHANTS.keys())
        )

        merchant = random.choice(
            MERCHANTS[category]
        )

        fraud_hour = generate_fraud_hour()

        txn_time = base_time + timedelta(
            seconds=random.randint(10, 90)
        )

        txn_time = txn_time.replace(
            hour=fraud_hour
        )

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
            random.choice([
                "android",
                "ios",
                "web"
            ]),

            "device_id":
            "DEVICE_" + str(uuid.uuid4())[:8],

            "timestamp":
            txn_time,

            "remaining_balance":
            new_balance,

            "fraud_label":
            1,

            "fraud_type":
            "velocity_fraud"
        }

        user["balance"] = new_balance

        user["transaction_history"].append(
            transaction
        )

        transactions.append(
            transaction
        )

    return transactions


# ============================================
# GRADUAL DRAINING FRAUD
# ============================================

def generate_gradual_draining_fraud(user):

    amount = round(

        user["balance"] * random.uniform(
            0.01,
            0.03
        ),

        2
    )

    if amount < 50:

        return None

    old_balance = user["balance"]

    if old_balance < amount:

        return None

    new_balance = round(

        old_balance - amount,

        2
    )

    category = random.choice([
        "grocery",
        "restaurants"
    ])

    merchant = random.choice(
        MERCHANTS[category]
    )

    location = random.choice(
        user["trusted_locations"]
    )

    timestamp = datetime.now()

    fraud_hour = generate_fraud_hour()

    timestamp = timestamp.replace(
        hour=fraud_hour
    )

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
        random.choice([
            "android",
            "ios",
            "web"
        ]),

        "device_id":
        "DEVICE_" + str(uuid.uuid4())[:8],

        "timestamp":
        timestamp,

        "remaining_balance":
        new_balance,

        "fraud_label":
        1,

        "fraud_type":
        "gradual_draining"
    }

    user["balance"] = new_balance

    user["transaction_history"].append(
        transaction
    )

    return transaction
# ============================================
# BEHAVIORAL CLONING FRAUD
# ============================================

def generate_behavior_cloning_fraud(user):

    if len(user["transaction_history"]) == 0:

        return None

    historical_txn = random.choice(
        user["transaction_history"]
    )

    avg_amount = user[
        "avg_transaction_amount"
    ]

    amount = round(

        random.uniform(

            avg_amount * 0.8,

            avg_amount * 1.2
        ),

        2
    )

    old_balance = user["balance"]

    if old_balance < amount:

        return None

    new_balance = round(

        old_balance - amount,

        2
    )

    category = historical_txn[
        "merchant_category"
    ]

    merchant = historical_txn[
        "merchant"
    ]

    # ============================================
    # MOSTLY TRUSTED LOCATION
    # ============================================

    if random.random() < 0.20:

        location = random.choice(
            FOREIGN_LOCATIONS
        )

    else:

        location = random.choice(
            user["trusted_locations"]
        )

    # ============================================
    # DEVICE CLONING
    # ============================================

    if random.random() < 0.70:

        device_id = random.choice(
            user["trusted_devices"]
        )

    else:

        device_id = (
            "DEVICE_" +
            str(uuid.uuid4())[:8]
        )

    timestamp = datetime.now()

    fraud_hour = generate_fraud_hour()

    timestamp = timestamp.replace(
        hour=fraud_hour
    )

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
        random.choice([
            "android",
            "ios",
            "web"
        ]),

        "device_id":
        device_id,

        "timestamp":
        timestamp,

        "remaining_balance":
        new_balance,

        "fraud_label":
        1,

        "fraud_type":
        "behavior_cloning"
    }

    user["balance"] = new_balance

    user["transaction_history"].append(
        transaction
    )

    return transaction
# ============================================
# ADAPTIVE FRAUD
# ============================================

def generate_adaptive_fraud(user):

    avg_amount = user[
        "avg_transaction_amount"
    ]

    # ============================================
    # FRAUDSTER TRIES TO STAY CLOSE
    # TO USER SPENDING PATTERN
    # ============================================

    amount = round(

        random.uniform(

            avg_amount * 0.9,

            avg_amount * 1.3
        ),

        2
    )

    old_balance = user["balance"]

    if old_balance < amount:

        return None

    new_balance = round(

        old_balance - amount,

        2
    )

    # ============================================
    # USE USER'S HISTORICAL BEHAVIOR
    # ============================================

    if len(user["transaction_history"]) > 0:

        historical_txn = random.choice(

            user["transaction_history"]
        )

        category = historical_txn[
            "merchant_category"
        ]

        merchant = historical_txn[
            "merchant"
        ]

    else:

        category = random.choice(
            list(MERCHANTS.keys())
        )

        merchant = random.choice(
            MERCHANTS[category]
        )

    # ============================================
    # MOSTLY DOMESTIC
    # ============================================

    if random.random() < 0.15:

        location = random.choice(
            FOREIGN_LOCATIONS
        )

    else:

        location = random.choice(
            user["trusted_locations"]
        )

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
    # HUMAN-LIKE TEMPORAL EVOLUTION
    # ============================================

    if len(user["transaction_history"]) > 0:

        previous_time = user[
            "transaction_history"
        ][-1]["timestamp"]

        # ============================================
        # ADAPTIVE FRAUD IS CAREFUL
        # ============================================

        gap_minutes = random.randint(
            15,
            180
        )

        timestamp = previous_time + timedelta(
            minutes=gap_minutes
        )

    else:

        timestamp = datetime.now()

    # ============================================
    # DEVICE TYPE
    # ============================================

    device_type = random.choice([

        "android",

        "ios",

        "web"
    ])

    # ============================================
    # FEATURE ENGINEERING
    # ============================================

    transaction_gap_seconds = 0

    previous_transaction_time = timestamp

    if len(user["transaction_history"]) > 0:

        previous_transaction_time = user[
            "transaction_history"
        ][-1]["timestamp"]

        transaction_gap_seconds = int(

            (
                timestamp -

                previous_transaction_time
            ).total_seconds()
        )

    transactions_last_5min = 0

    for txn in user["transaction_history"]:

        time_difference = (

            timestamp -

            txn["timestamp"]

        ).total_seconds()

        if time_difference <= 300:

            transactions_last_5min += 1

    amount_balance_ratio = round(

        amount / (old_balance + 1),

        4
    )

    is_high_amount = int(

        amount >

        avg_amount * 1.8
    )

    device_change = int(

        device_id not in
        user["trusted_devices"]
    )

    # ============================================
    # CREATE TRANSACTION
    # ============================================

    transaction = {

        "timestamp":
        timestamp,

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

        "old_balance":
        old_balance,

        "new_balance":
        new_balance,

        "remaining_balance":
        new_balance,

        "account_age_days":
        user["account_age_days"],

        "daily_transaction_count":
        random.randint(1, 10),

        "fraud_label":
        1,

        "fraud_type":
        "adaptive_fraud",

        "time_since_last_transaction":
        transaction_gap_seconds,

        "is_foreign_transaction":
        int(location in FOREIGN_LOCATIONS),

        "amount_balance_ratio":
        amount_balance_ratio,

        "is_high_amount":
        is_high_amount,

        "transaction_hour":
        timestamp.hour,

        "is_night_transaction":
        int(timestamp.hour <= 5),

        "device_change":
        device_change,

        "previous_transaction_time":
        previous_transaction_time,

        "transaction_gap_seconds":
        transaction_gap_seconds,

        "rapid_transaction":
        int(transaction_gap_seconds < 300),

        "transactions_last_5min":
        transactions_last_5min
    }

    # ============================================
    # UPDATE USER STATE
    # ============================================

    user["balance"] = new_balance

    user["transaction_history"].append(
        transaction
    )

    return transaction