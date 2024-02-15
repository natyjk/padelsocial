insert into jugadores_unicos(nombre_jugador, nombre, apellido)
select
    j.nombre_jugador,
    '' as nombre,
    '' as aellido
from
    jugadores j
left join
    jugadores_unicos ju
    on j.nombre_jugador = ju.nombre_jugador
where
    j.nombre_jugador <> ''
    and ju.nombre_jugador is null;