with base_series as (
    -- Geração de uma tabela de números rápida e ultra leve (Tally Table)
    select 0 as g union all select 0
),
lv1 as (select 0 as g from base_series a cross join base_series b), -- 4 linhas
lv2 as (select 0 as g from lv1 a cross join lv1 b),                 -- 16 linhas
lv3 as (select 0 as g from lv2 a cross join lv2 b),                 -- 256 linhas
lv4 as (select 0 as g from lv3 a cross join lv3 b),                 -- 65.536 linhas (cobre mais de 150 anos)
nums as (
    select row_number() over (order by (select null)) - 1 as n 
    from lv4
),
dates as (
    select 
        -- Definindo a janela temporal do seu projeto (De 2015 até 2030)
        cast(dateadd(day, n, '2015-01-01') as date) as data_base
    from nums
    where n <= datediff(day, '2015-01-01', '2030-12-31')
),
extracted_attributes as (
    select
        data_base,
        -- Chave Inteligente de Data (Formato INT YYYYMMDD - Ideal para performance e Joins)
        year(data_base) * 10000 + month(data_base) * 100 + day(data_base) as date_key,
        year(data_base) as ano,
        month(data_base) as mes_num,
        
        -- Nome do mês com a primeira letra em maiúscula (Garante pt-BR independente do idioma do servidor)
        upper(left(format(data_base, 'MMMM', 'pt-BR'), 1)) + substring(format(data_base, 'MMMM', 'pt-BR'), 2, 50) as mes_nome,
        
        day(data_base) as dia,
        datepart(dayofyear, data_base) as dia_do_ano,
        
        -- Dia da semana numérico universal (1 = Segunda-feira, 7 = Domingo) blindado contra @@DATEFIRST do SQL Server
        case ((datepart(dw, data_base) + @@DATEFIRST - 1) % 7)
            when 0 then 7
            else ((datepart(dw, data_base) + @@DATEFIRST - 1) % 7)
        end as dia_da_semana_num,
        
        -- Nome do dia da semana com a primeira letra em maiúscula
        upper(left(format(data_base, 'dddd', 'pt-BR'), 1)) + substring(format(data_base, 'dddd', 'pt-BR'), 2, 50) as dia_da_semana_nome,
        
        datepart(quarter, data_base) as trimestre,
        case when month(data_base) <= 6 then 1 else 2 end as semestre,
        
        -- Flag de Fim de Semana (1 = Sim, 0 = Não)
        case when ((datepart(dw, data_base) + @@DATEFIRST - 1) % 7) in (0, 6) then 1 else 0 end as flag_fim_de_semana
    from dates
),
holidays as (
    select
        *,
        -- Mapeamento Automatizado de Feriados Nacionais Fixos (Brasil)
        case 
            when mes_num = 1 and dia = 1 then 'Ano Novo'
            when mes_num = 4 and dia = 21 then 'Tiradentes'
            when mes_num = 5 and dia = 1 then 'Dia do Trabalho'
            when mes_num = 9 and dia = 7 then 'Independência do Brasil'
            when mes_num = 10 and dia = 12 then 'Nossa Senhora Aparecida'
            when mes_num = 11 and dia = 2 then 'Finados'
            when mes_num = 11 and dia = 15 then 'Proclamação da República'
            when mes_num = 12 and dia = 25 then 'Natal'
            else null
        end as feriado_nome
    from extracted_attributes
),
final as (
    select
        date_key,
        data_base as data,
        ano,
        mes_num,
        mes_nome,
        dia,
        dia_do_ano,
        dia_da_semana_num,
        dia_da_semana_nome,
        trimestre,
        semestre,
        flag_fim_de_semana,
        case when feriado_nome is not null then 1 else 0 end as flag_feriado,
        feriado_nome,
        
        -- Métrica de Dia Útil pedida: Não pode ser fim de semana E não pode ser feriado
        case 
            when flag_fim_de_semana = 1 or feriado_nome is not null then 0 
            else 1 
        end as flag_dia_util
    from holidays
)

select * from final