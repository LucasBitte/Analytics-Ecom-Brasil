with source as (
    select * from {{ source('olist', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_status as status,
        cast(order_purchase_timestamp as datetime2) as purchase_at,
        cast(order_approved_at as datetime2) as approved_at,
        cast(order_delivered_carrier_date as datetime2) as delivered_carrier_at,
        cast(order_delivered_customer_date as datetime2) as delivered_customer_at,
        cast(order_estimated_delivery_date as datetime2) as estimated_delivery_at
    from source
)

select * from renamed