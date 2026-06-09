with source as (
    select
        product_id,
        product_category_name,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm,
        product_photos_qty
    from {{ source('olist', 'products') }}
),

cleaned as (
    select
        product_id,
        product_category_name,
        coalesce(product_weight_g, 0) as product_weight_g,
        coalesce(product_length_cm, 0) as product_length_cm,
        coalesce(product_height_cm, 0) as product_height_cm,
        coalesce(product_width_cm, 0) as product_width_cm,
        coalesce(product_photos_qty, 0) as product_photos_qty
    from source
    where product_id is not null
)

select * from cleaned
