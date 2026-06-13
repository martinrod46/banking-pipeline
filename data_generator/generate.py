import random
import time
import psycopg2
from faker import Faker
from datetime import datetime

fake = Faker()

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="banking_db",
    user="banking_user",
    password="banking_pass"
)
conn.autocommit = True
cursor = conn.cursor()

def create_customer():
    cursor.execute("""
        INSERT INTO customers 
            (first_name, last_name, email, phone, address, city, country, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING customer_id
    """, (
        fake.first_name(),
        fake.last_name(),
        fake.unique.email(),
        fake.phone_number()[:20],
        fake.street_address(),
        fake.city(),
        fake.country()[:50],
        fake.date_of_birth(minimum_age=18, maximum_age=80)
    ))
    return cursor.fetchone()[0]

def create_account(customer_id):
    cursor.execute("""
        INSERT INTO accounts 
            (customer_id, account_type, account_status, balance, currency)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING account_id
    """, (
        customer_id,
        random.choice(['checking', 'savings', 'credit']),
        'active',
        round(random.uniform(100, 50000), 2),
        'USD'
    ))
    return cursor.fetchone()[0]

def create_transaction(account_id):
    amount = round(random.uniform(1, 5000), 2)
    cursor.execute("""
        INSERT INTO transactions 
            (account_id, transaction_type, amount, currency, description, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING transaction_id
    """, (
        account_id,
        random.choice(['deposit', 'withdrawal', 'transfer', 'payment']),
        amount,
        'USD',
        fake.sentence(nb_words=4),
        random.choice(['completed', 'completed', 'completed', 'pending', 'failed'])
    ))
    return cursor.fetchone()[0]

def create_fraud_flag(transaction_id):
    cursor.execute("""
        INSERT INTO fraud_flags (transaction_id, flag_reason)
        VALUES (%s, %s)
    """, (
        transaction_id,
        random.choice([
            'Unusual transaction amount',
            'Multiple transactions in short period',
            'Transaction from unusual location',
            'Exceeded daily limit'
        ])
    ))

def update_customer(customer_id):
    """Simulate customer updating their info - this is what triggers SCD2!"""
    cursor.execute("""
        UPDATE customers 
        SET address = %s, city = %s, updated_at = %s
        WHERE customer_id = %s
    """, (
        fake.street_address(),
        fake.city(),
        datetime.now(),
        customer_id
    ))
    print(f"  → Customer {customer_id} moved to a new address! (SCD2 trigger)")

def run():
    print("🏦 Banking data generator started!")
    print("   Ctrl+C to stop\n")

    customer_ids = []
    account_ids = []

    # Initial seed - create 10 customers with accounts
    print("Creating initial customers and accounts...")
    for _ in range(10):
        cid = create_customer()
        aid = create_account(cid)
        customer_ids.append(cid)
        account_ids.append(aid)
        print(f"  ✅ Customer {cid} created with account {aid}")

    print("\n🔄 Starting real-time transaction simulation...\n")

    cycle = 0
    while True:
        cycle += 1
        print(f"--- Cycle {cycle} ---")

        # Generate 3-7 transactions per cycle
        for _ in range(random.randint(3, 7)):
            account_id = random.choice(account_ids)
            txn_id = create_transaction(account_id)

            # 10% chance of fraud flag
            if random.random() < 0.10:
                create_fraud_flag(txn_id)
                print(f"  🚨 Transaction {txn_id} flagged for fraud!")
            else:
                print(f"  💸 Transaction {txn_id} on account {account_id}")

        # Every 5 cycles add a new customer
        if cycle % 5 == 0:
            cid = create_customer()
            aid = create_account(cid)
            customer_ids.append(cid)
            account_ids.append(aid)
            print(f"  👤 New customer {cid} joined!")

        # Every 7 cycles simulate a customer updating their info
        if cycle % 7 == 0:
            update_customer(random.choice(customer_ids))

        time.sleep(2)  # Wait 2 seconds between cycles

if __name__ == "__main__":
    run()