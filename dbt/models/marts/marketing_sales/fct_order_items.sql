with order_items as (
    select * from {{ ref('stg_olist__order_items') }}
),

final as (
    select
        -- 1. Chave Primária Composta da Fato de Itens
        {{ dbt_utils.generate_surrogate_key(['order_id', 'order_item_id']) }} as order_item_sk,
        order_id,
        order_item_id,

        -- 2. Chaves Estrangeiras (Geradas via Hash para linkar com as dimensões)
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_sk,
        {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_sk,
        {{ dbt_utils.generate_surrogate_key(['seller_id']) }} as seller_sk,

        -- 3. Métricas Financeiras (Campos numéricos exatos que vieram da Staging)
        shipping_limit_at,
        price_amount,
        freight_amount,
        
        -- Métrica derivada: Custo total do item para o bolso do cliente
        (price_amount + freight_amount) as total_item_amount

    from order_items
)

select * from final