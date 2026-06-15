with
  corridas_2026 as (
    select
      id_corrida
    from
      {{ ref('silver_sessoes') }}
    where
      ano = 2026
      and nome_sessao in ('Race', 'Sprint')
  )
select distinct
  url_foto,
  numero_piloto,
  nome_completo,
  abreviacao_nome,
  equipe
from
  {{ ref('silver_pilotos') }}
where
  1 = 1
  and url_foto is not null
  and id_corrida in (
    select
      *
    from
      corridas_2026
  )
order by
  numero_piloto asc