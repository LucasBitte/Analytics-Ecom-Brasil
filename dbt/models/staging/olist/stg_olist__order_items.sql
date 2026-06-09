with source as (
    select * from {{ source('olist', 'order_items') }}
),

renamed as (
    select
        order_id,
        order_item_id,
        product_id,
        seller_id,
        cast(shipping_limit_date as datetime2) as shipping_limit_at,
        cast(price as decimal(10,2)) as price_amount,
        cast(freight_value as decimal(10,2)) as freight_amount
    from source
)

select * from renamed