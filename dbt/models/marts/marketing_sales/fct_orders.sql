with orders as (
    select * from {{ ref('stg_olist__orders') }}
),

final as (
    select
        -- 1. Chave Primária da Fato
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_sk,
        order_id,

        -- 2. Chaves Estrangeiras (Links com as Dimensões)
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk,
        
        -- 3. Histórico de Status e Datas (Métricas Temporais)
        status,
        purchase_at,
        approved_at,
        delivered_carrier_at,
        delivered_customer_at,
        estimated_delivery_at,

        -- 4. Métricas Derivadas de Performance de Entrega 
        datediff(day, purchase_at, delivered_customer_at) as tempo_entrega_real_dias,
        datediff(day, purchase_at, estimated_delivery_at) as tempo_entrega_estimado_dias,
        
        -- Flag para indicar se o pedido atrasou ou chegou antes do prazo
        case 
            when delivered_customer_at > estimated_delivery_at then 1 
            else 0 
        end as flag_pedido_atrasado

    from orders
)

select * from final