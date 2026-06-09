with sellers as (
    select * from {{ ref('stg_olist__sellers') }}
),

final as (
    select
        -- Gerando a Surrogate Key do Vendedor via Hash MD5
        {{ dbt_utils.generate_surrogate_key(['seller_id']) }} as seller_sk,
        seller_id,
        zip_code_prefix,
        city,
        state
    from sellers
)

select * from final