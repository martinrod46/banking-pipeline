with source as (
    select * from {{ source('banking_raw', 'transactions') }}
),

cleaned as (
    select
        transaction_id,
        account_id,
        transaction_type,
        amount,
        currency,
        description,
        status,
        created_at,

        -- derived fields
        case 
            when amount >= 1000 then 'high'
            when amount >= 100  then 'medium'
            else 'low'
        end as amount_category,

        case
            when status = 'failed' then true
            else false
        end as is_failed

    from source
    where transaction_id is not null
)

select * from cleaned
