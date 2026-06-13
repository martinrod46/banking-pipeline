with source as (
    select * from {{ source('banking_raw', 'customers') }}
),

cleaned as (
    select
        customer_id,
        first_name,
        last_name,
        email,
        phone,
        address,
        city,
        country,
        date_of_birth,
        created_at,
        updated_at,

        -- derived fields
        concat(first_name, ' ', last_name) as full_name,
        date_diff(current_date(), date_of_birth, year) as age

    from source
    where customer_id is not null
)

select * from cleaned
