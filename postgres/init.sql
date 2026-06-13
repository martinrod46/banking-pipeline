-- CUSTOMERS
CREATE TABLE customers (
    customer_id     SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    phone           VARCHAR(20),
    address         VARCHAR(200),
    city            VARCHAR(50),
    country         VARCHAR(50),
    date_of_birth   DATE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ACCOUNTS
CREATE TABLE accounts (
    account_id      SERIAL PRIMARY KEY,
    customer_id     INT REFERENCES customers(customer_id),
    account_type    VARCHAR(20) CHECK (account_type IN ('checking', 'savings', 'credit')),
    account_status  VARCHAR(20) CHECK (account_status IN ('active', 'inactive', 'blocked')),
    balance         NUMERIC(15,2) DEFAULT 0.00,
    currency        VARCHAR(3) DEFAULT 'USD',
    opened_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTIONS
CREATE TABLE transactions (
    transaction_id      SERIAL PRIMARY KEY,
    account_id          INT REFERENCES accounts(account_id),
    transaction_type    VARCHAR(20) CHECK (transaction_type IN ('deposit', 'withdrawal', 'transfer', 'payment')),
    amount              NUMERIC(15,2) NOT NULL,
    currency            VARCHAR(3) DEFAULT 'USD',
    description         VARCHAR(200),
    status              VARCHAR(20) CHECK (status IN ('pending', 'completed', 'failed', 'reversed')),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FRAUD FLAGS (bonus table - makes the project interesting!)
CREATE TABLE fraud_flags (
    flag_id         SERIAL PRIMARY KEY,
    transaction_id  INT REFERENCES transactions(transaction_id),
    flag_reason     VARCHAR(200),
    flagged_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved        BOOLEAN DEFAULT FALSE
);