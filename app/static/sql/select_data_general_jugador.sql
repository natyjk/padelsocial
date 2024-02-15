select
    j.id_jugador_unico,
    j.nombre_completo,
    j.nombre,
    j.apellido,
    count(distinct concat(p.nombre_torneo,p.categoria)) as torneos_jugados,
    count(distinct p.categoria) as categorias_jugadas,
    count(distinct concat(p.nombre_torneo,p.categoria,p.nombre_partido)) as total_partidos_jugados,
    count(distinct
        case when (j.nombre_jugador_var in (p.jugador1_pareja1, p.jugador2_pareja1) and p.pareja_ganadora = 'Pareja 1')
            or (j.nombre_jugador_var in (p.jugador1_pareja2, p.jugador2_pareja2) and p.pareja_ganadora = 'Pareja 2')
        then concat(p.nombre_torneo,p.categoria,p.nombre_partido)
        end) as partidos_ganados,
    sum(case when p.nombre_partido = 'Final' then 1 else 0 end) as finales_jugadas,
    sum(case when p.nombre_partido = 'Final' and
        ((j.nombre_jugador_var in (jugador1_pareja1, jugador2_pareja1) and p.pareja_ganadora = 'Pareja 1')
            or (j.nombre_jugador_var in (jugador1_pareja2, jugador2_pareja2) and p.pareja_ganadora = 'Pareja 2'))
    then 1 else 0 end) as finales_ganadas
from
    (-- j
    select
        ju.id_jugador_unico,
        ju.nombre_completo,
        ju.nombre,
        ju.apellido,
        uj.id_jugador,
        j.nombre_jugador as nombre_jugador_var
    from
        jugadores_unicos ju
    left join
        union_jugadores uj
        on ju.id_jugador_unico = uj.id_jugador_unico
    left join
        jugadores j
        on j.id_jugador = uj.id_jugador
    where
        ju.id_jugador_unico = {}
    )j
inner join
    partidos_v2 p
    on j.nombre_jugador_var in (p.jugador1_pareja1, p.jugador2_pareja1, p.jugador1_pareja2, p.jugador2_pareja2)
group by
    1,2,3,4;
