with source as (
    select * from {{ source('olist', 'product_categories') }}
),

renamed as (
    select
        product_category_name as category_name,
        product_category_name_english as category_name_english
    from source
)

select * from renamed