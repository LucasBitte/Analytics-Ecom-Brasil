with geo as (
    select * from {{ ref('stg_olist__geolocation') }}
),

-- Agrupando por CEP para garantir a unicidade da Dimensão
aggregated as (
    select
        zip_code_prefix,
        city,
        state,
        avg(latitude) as latitude,
        avg(longitude) as longitude
    from geo
    group by zip_code_prefix, city, state
),

final as (
    select
        -- Criando a Chave Substituta do CEP
        {{ dbt_utils.generate_surrogate_key(['zip_code_prefix']) }} as geolocation_sk,
        zip_code_prefix,
        city,
        state,
        latitude,
        longitude
    from aggregated
)

select * from final