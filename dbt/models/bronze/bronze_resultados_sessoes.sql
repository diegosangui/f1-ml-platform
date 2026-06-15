select
  position,
  driver_number,
  number_of_laps,
  dnf,
  dns,
  dsq,
  duration,
  gap_to_leader,
  meeting_key,
  session_key,
  points
from {{ source('raw', 'resultados_sessoes') }}