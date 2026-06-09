with payments as (
    select * from {{ ref('stg_olist__order_payments') }}
),

final as (
    select
        -- 1. Chave Primária da Fato de Pagamentos
        {{ dbt_utils.generate_surrogate_key(['order_id', 'payment_sequential']) }} as payment_sk,
        
        -- 2. Chave Estrangeira para conectar com a fct_orders
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_sk,
        order_id,
        
        -- 3. Atributos e Métricas
        payment_sequential,
        payment_type,
        payment_installments,
        payment_amount

    from payments
)

select * from final