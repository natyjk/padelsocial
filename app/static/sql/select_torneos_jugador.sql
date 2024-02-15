
select
    j.nombre_completo,
    cast(t.fecha_ano as int)*100 + cast(t.fecha_mes as int) as month_id,
    t.fecha_str,
    t.fecha_ano,
    t.lugar,
    t.nombre_torneo,
    p.categoria,
    case
        when j.nombre_jugador_var = p.jugador1_pareja1 then p.jugador2_pareja1
        when j.nombre_jugador_var = p.jugador2_pareja1 then p.jugador1_pareja1
        when j.nombre_jugador_var = p.jugador1_pareja2 then p.jugador2_pareja2
        when j.nombre_jugador_var = p.jugador2_pareja2 then p.jugador1_pareja2
    end as pareja,
    count(distinct p.nombre_partido) as total_partidos_jugados,
    count(distinct
        case when (j.nombre_jugador_var in (p.jugador1_pareja1, p.jugador2_pareja1) and p.pareja_ganadora = 'Pareja 1')
            or (j.nombre_jugador_var in (p.jugador1_pareja2, p.jugador2_pareja2) and p.pareja_ganadora = 'Pareja 2')
        then p.nombre_partido
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
        uj.id_jugador_unico,
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
inner join
    torneos t
    on p.id_torneo = t.id_torneo
group by
    1,2,3,4,5,6,7,8
order by
    2 desc;