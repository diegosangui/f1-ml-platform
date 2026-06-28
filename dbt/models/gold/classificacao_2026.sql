with
  corridas_2026 as (
    select
      id_sessao,
      nome_sessao
    from
      {{ ref('silver_sessoes') }}
    where
      ano = 2026
      and nome_sessao in ('Race', 'Sprint')
  ),
  vitorias as (
    select
      numero_piloto,
      count(*) as num_vitoria
    from
      {{ ref('silver_resultadosessoes') }}
    where
      id_sessao in (
        select
          id_sessao
        from
          corridas_2026
        where
          nome_sessao in ('Race')
      )
      and posicao = 1
    group by
      numero_piloto
  ),
  ponto_piloto as (
    select
      numero_piloto,
      sum(pontos) as pontos_total
    from
      {{ ref('silver_resultadosessoes') }}
    where
      id_sessao in (
        select
          id_sessao
        from
          corridas_2026
      )
    group by
      numero_piloto
    order by
      pontos_total desc
  ),
  pilotos as (
    select
      url_foto,
      numero_piloto,
      nome_completo,
      equipe
    from
      {{ ref('silver_pilotos') }}
    where
      id_sessao in (
        select
          id_sessao
        from
          corridas_2026
      )
  ),
  classificacao as (
    select distinct
      pil.url_foto,
      pp.numero_piloto,
      initcap(pil.nome_completo) as nome_completo,
      pil.equipe,
      pp.pontos_total
    from
      ponto_piloto pp
      left join pilotos pil on (pp.numero_piloto = pil.numero_piloto)
    order by
      pp.pontos_total desc
  )
select
  row_number() over (
    order by
      (
        select
          null
      )
  ) as posicao,
  cla.url_foto,
  --cla.numero_piloto,
  case
    when vit.num_vitoria is null then 0
    else vit.num_vitoria
  end as num_vitoria,
  cla.nome_completo,
  cla.equipe,
  cla.pontos_total
from
  classificacao cla
  left join vitorias vit on (cla.numero_piloto = vit.numero_piloto)