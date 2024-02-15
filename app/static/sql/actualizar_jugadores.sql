insert into jugadores(nombre_jugador)
(
select distinct nombre_jugador
from
(
with jugador as
(
select
    p.jugador1_pareja1,
    p.jugador2_pareja1,
    p.jugador1_pareja2,
    p.jugador2_pareja2
from
    partidos_v2 p
)

select
    distinct a.jugador as nombre_jugador
from
    (
    select
        distinct jugador1_pareja1 as jugador
    from
        jugador

    union all

    select
        distinct jugador2_pareja1 as jugador
    from
        jugador

    union all

    select
        distinct jugador1_pareja2 as jugador
    from
        jugador

    union all

    select
        distinct jugador2_pareja2 as jugador
    from
        jugador
    )a
left join
    jugadores j
    on j.nombre_jugador = a.jugador
where
    j.nombre_jugador is null

)b
)