with stg_products as (
    select * from {{ ref('stg_olist__products') }}
),

product_categories as (
    select
        product_category_name,
        product_category_name_english
    from {{ source('olist', 'product_categories') }}
),

enriched as (
    select
        {{ dbt_utils.generate_surrogate_key(['stg_products.product_id']) }} as product_sk,
        stg_products.product_id as product_key,
        pc.product_category_name_english as product_category,
        stg_products.product_weight_g,
        stg_products.product_length_cm,
        stg_products.product_height_cm,
        stg_products.product_width_cm,
        stg_products.product_photos_qty,
        cast(getdate() as date) as load_date,
        1 as is_active
    from stg_products
    left join product_categories as pc
        on stg_products.product_category_name = pc.product_category_name
)

select * from enriched
