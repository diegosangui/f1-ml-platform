select 
  meeting_key::integer as id_corrida,
  session_key::integer as id_sessao,
  driver_number::integer as numero_piloto,
  broadcast_name::text as nome_transmissao,
  full_name::text as nome_completo,
  name_acronym::text as abreviacao_nome,
  team_name::text as equipe,
  team_colour::text as cor_equipe,
  first_name::text as nome,
  last_name::text as sobrenome,
  headshot_url::text as url_foto
from {{ ref('bronze_pilotos') }}
