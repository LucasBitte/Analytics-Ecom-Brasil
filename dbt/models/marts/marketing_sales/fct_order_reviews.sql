with reviews as (
    select * from {{ ref('stg_olist__order_reviews') }}
),

final as (
    select
        -- 1. Chave Primária da Fato de Avaliações
        {{ dbt_utils.generate_surrogate_key(['review_id', 'order_id']) }} as review_sk,
        review_id,

        -- 2. Chave Estrangeira para conectar com a fct_orders
        {{ dbt_utils.generate_surrogate_key(['order_id']) }} as order_sk,
        order_id,

        -- 3. Métricas e Atributos de Satisfação
        review_score as csat_score,
        comment_title,
        comment_message,
        created_at,
        answered_at,

        -- Métrica derivada: Tempo que o cliente levou para avaliar/responder em horas
        datediff(hour, created_at, answered_at) as tempo_resposta_avaliacao_horas

    from reviews
)

select * from final