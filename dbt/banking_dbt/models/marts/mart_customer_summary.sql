with customers as (
    select * from {{ ref('stg_customers') }}
),

transactions as (
    select * from {{ ref('stg_transactions') }}
),

accounts as (
    select * from {{ source('banking_raw', 'accounts') }}
),

customer_transactions as (
    select
        c.customer_id,
        c.full_name,
        c.age,
        c.city,
        c.country,
        count(t.transaction_id)                     as total_transactions,
        sum(t.amount)                               as total_amount_spent,
        avg(t.amount)                               as avg_transaction_amount,
        sum(case when t.is_failed then 1 else 0 end) as failed_transactions,
        sum(case when t.amount_category = 'high' 
            then 1 else 0 end)                      as high_value_transactions,
        max(t.created_at)                           as last_transaction_date

    from customers c
    left join accounts a on c.customer_id = a.customer_id
    left join transactions t on a.account_id = t.account_id
    group by 1,2,3,4,5
)

select * from customer_transactions
