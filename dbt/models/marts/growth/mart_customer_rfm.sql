{{ config(
    materialized='table',
    schema='analytics'
) }}

with customers as (
    select * from {{ ref('dim_customers') }}
),

orders as (
    select * from {{ ref('fct_orders') }}
),

order_items as (
    select 
        order_sk,
        sum(total_item_amount) as total_order_amount
    from {{ ref('fct_order_items') }}
    group by order_sk
),

customer_behavior as (
    select
        c.customer_unique_id,
        max(o.purchase_at) as last_purchase_at,
        count(distinct o.order_id) as total_orders,
        sum(coalesce(i.total_order_amount, 0)) as total_spent
    from customers c
    inner join orders o on c.customer_sk = o.customer_sk
    left join order_items i on o.order_sk = i.order_sk
    group by c.customer_unique_id
),

rfm_raw as (
    select
        customer_unique_id,
        datediff(day, last_purchase_at, (select max(purchase_at) from orders)) as recency_days,
        total_orders as frequency,
        total_spent as monetary
    from customer_behavior
),

rfm_scores as (
    select
        customer_unique_id,
        recency_days,
        frequency,
        monetary,
        ntile(5) over (order by recency_days desc) as r_score,
        
        -- Nossa regra hibrida blindada contra a distorcao do NTILE
        case 
            when frequency = 1 then 1
            when frequency = 2 then 3
            else 5
        end as f_score,
        
        ntile(5) over (order by monetary asc) as m_score
    from rfm_raw
),

final as (
    select
        customer_unique_id,
        recency_days,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        cast((r_score + f_score + m_score) / 3.0 as decimal(10,2)) as rfm_score_average,
        case
            when r_score >= 4 and f_score >= 4 and m_score >= 4 then 'Campeões (Clientes VIP)'
            when r_score >= 3 and f_score >= 3 and m_score >= 3 then 'Clientes Leais'
            when r_score >= 4 and f_score >= 2 and m_score >= 2 then 'Potenciais Leais'
            when r_score >= 4 and f_score = 1 then 'Novos Clientes'
            when r_score <= 2 and f_score >= 4 and m_score >= 4 then 'Não Podemos Perder'
            when r_score <= 2 and f_score >= 2 and m_score >= 2 then 'Clientes em Risco'
            when r_score = 3 and f_score >= 2 and m_score >= 2 then 'Precisam de Atenção'
            when r_score = 2 and f_score <= 2 and m_score <= 2 then 'Prestes a Dormir'
            when r_score = 2 and f_score <= 2 then 'Hibernando'
            else 'Clientes Perdidos / Inativos'
        END as customer_segmentation
    from rfm_scores
)

select * from final