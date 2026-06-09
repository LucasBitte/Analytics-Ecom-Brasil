with customers as (
    select * from {{ ref('stg_olist__customers') }}
),

final as (
    select
        -- Gerando a Surrogate Key sênior via Hash MD5
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk,
        customer_id,
        customer_unique_id,
        zip_code_prefix,
        city,
        state
    from customers
)

select * from final