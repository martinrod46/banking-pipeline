with fraud as (
    select * from {{ ref('stg_fraud_flags') }}
),

transactions as (
    select * from {{ ref('stg_transactions') }}
),

fraud_analysis as (
    select
        t.transaction_type,
        t.amount_category,
        count(f.flag_id)                            as total_flags,
        sum(case when f.flag_status = 'open' 
            then 1 else 0 end)                      as open_flags,
        sum(case when f.flag_status = 'resolved' 
            then 1 else 0 end)                      as resolved_flags,
        avg(t.amount)                               as avg_flagged_amount,
        max(t.amount)                               as max_flagged_amount

    from fraud f
    join transactions t on f.transaction_id = t.transaction_id
    group by 1,2
)

select * from fraud_analysis
