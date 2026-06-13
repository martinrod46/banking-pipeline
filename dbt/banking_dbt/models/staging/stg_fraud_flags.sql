with source as (
    select * from {{ source('banking_raw', 'fraud_flags') }}
),

cleaned as (
    select
        flag_id,
        transaction_id,
        flag_reason,
        flagged_at,
        resolved,

        -- derived fields
        case
            when resolved = true then 'resolved'
            else 'open'
        end as flag_status

    from source
    where flag_id is not null
)

select * from cleaned
