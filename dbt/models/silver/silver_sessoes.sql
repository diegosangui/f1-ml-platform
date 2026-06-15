select
  session_key::integer as id_sessao,
  session_type::text as tipo_sessao,
  session_name::text as nome_sessao,
  date_start::date as data_inicio,
  date_end::date as data_fim,
  meeting_key::integer as id_corrida,
  circuit_key::integer as id_circuito,
  circuit_short_name::text as nome_circuito,
  country_key::integer as id_pais,
  country_code::text as codigo_pais,
  country_name::text as nome_pais,
  location::text as localizacao,
  gmt_offset::text offset_gmt,
  year::integer as ano,
  is_cancelled::boolean as cancelado
from {{ ref('bronze_sessoes') }}