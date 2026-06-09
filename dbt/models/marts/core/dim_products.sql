with products as (
    select * from {{ ref('stg_olist__products') }}
),

categories as (
    select * from {{ ref('stg_olist__product_categories') }}
),

final as (
    select
        -- Gerando a chave substituta do produto
        {{ dbt_utils.generate_surrogate_key(['products.product_id']) }} as product_sk,
        products.product_id,
        -- Se houver tradução usa em inglês, senão mantém o termo original em português
        coalesce(categories.category_name_english, products.category_name) as category_name,
        products.name_length,
        products.description_length,
        products.photos_qty,
        products.weight_g,
        products.length_cm,
        products.height_cm,
        products.width_cm
    from products
    left join categories
        on products.category_name = categories.category_name
)

select * from final