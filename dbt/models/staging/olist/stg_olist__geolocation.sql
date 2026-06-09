with source as (
    select * from {{ source('olist', 'geolocation') }}
),

renamed as (
    select
        -- Buscando os nomes físicos reais com prefixo e limpando para o padrão de negócios
        geolocation_zip_code_prefix as zip_code_prefix,
        geolocation_lat as latitude,
        geolocation_lng as longitude,
        geolocation_city as city,
        geolocation_state as state
    from source
)

select * from renamed