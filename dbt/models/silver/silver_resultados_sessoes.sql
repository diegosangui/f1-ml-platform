select
  position::integer as posicao,
  driver_number::integer as numero_piloto,
  number_of_laps::integer as numero_de_voltas,
  dnf::boolean as abandonou,
  dns::boolean as nao_largou,
  dsq::boolean as desclassificado,
  meeting_key::integer as id_corrida,
  session_key::integer as id_sessao,
  points::integer as pontos
from {{ ref('bronze_resultados_sessoes') }}