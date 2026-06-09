with source as (
    select * from {{ source('olist', 'products') }}
),

renamed as (
    select
        product_id,
        product_category_name as category_name,
        cast(product_name_lenght as smallint) as name_length,
        cast(product_description_lenght as smallint) as description_length,
        cast(product_photos_qty as tinyint) as photos_qty,
        product_weight_g as weight_g,
        product_length_cm as length_cm,
        product_height_cm as height_cm,
        product_width_cm as width_cm
    from source
)

select * from renamed