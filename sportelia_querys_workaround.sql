select *
from
(-- t
select 
    j.jugador,
    count(distinct j.nombre_torneo) as torneos_jugados,
    sum(j.total_partidos_jugados) as total_partidos_jugados,
    sum(j.partidos_ganados) as total_partidos_ganados,
    round(sum(j.partidos_ganados)*100/ sum(j.total_partidos_jugados)) as porcentaje_partidos_ganados,
    sum(j.finales_ganadas) as torneos_ganados,
    round(sum(j.finales_ganadas)*100 / count(distinct j.nombre_torneo)) as porcentaje_torneos_ganados
from    
    jugadores_agg_data j
where
    length(j.jugador) > 2
    and position('anador' in j.jugador) = 0
    and position('grupo' in j.jugador) = 0
    and j.jugador not in ('pendiente')
group by
    1
order by
    3 desc
)t
where
    t.jugador in ('neus lladó', 'natalie jelenkiewicz','carmen martínez', 'gonzalo mora', 'carol foresti',
    'marina gayà', 'laura martorell', 'carlota pou', 'patri antón', 'patricia nadal', 'miquela torrens', 'camila tealdo',
    'ana de la portilla', 'aina portas', 'inma ramirez ledesma')
    
    
    
select 
    td.id_torneo,
    td.token_torneo,
    td.nombre_torneo,
    td.lugar,
    td.fecha as fecha_str,
    '2023' as fecha_ano,
    count(*) as qty 
from
    torneos_df_2023 td
group by
    1,2,3,4,5
    
    
    
create table torneos as 
insert into torneos 
select 
    td.id_torneo,
    td.token_torneo,
    td.nombre_torneo,
    td.lugar,
    td.fecha as fecha_str,
    '2023' as fecha_ano,
    case 
         WHEN position('january' IN lower(td.fecha)) > 0 THEN 01
        WHEN position('february' IN lower(td.fecha)) > 0 THEN 02
        WHEN position('march' IN lower(td.fecha)) > 0 THEN 03
        WHEN position('april' IN lower(td.fecha)) > 0 THEN 04
        WHEN position('may' IN lower(td.fecha)) > 0 THEN 05
        WHEN position('june' IN lower(td.fecha)) > 0 THEN 06
        WHEN position('july' IN lower(td.fecha)) > 0 THEN 07
        WHEN position('august' IN lower(td.fecha)) > 0 THEN 08
        WHEN position('september' IN lower(td.fecha)) > 0 THEN 09
        WHEN position('october' IN lower(td.fecha)) > 0 THEN 10
        WHEN position('november' IN lower(td.fecha)) > 0 THEN 11
        WHEN position('december' IN lower(td.fecha)) > 0 THEN 12
        ELSE NULL 
    end as fecha_mes,     
    td.source
from
    torneos_df_202302 td
left join
    torneos t on t.id_torneo = td.id_torneo
where
    t.id_torneo is null
    

ALTER TABLE torneos
ADD CONSTRAINT pk_torneos PRIMARY KEY (id_torneo);


select 
    t.*,
    count(p.*) as partidos
from
    torneos t
left join
    partidos_df p
    on p.nombre_torneo = t.nombre_torneo
group by
    t.id_torneo
    
where
    t.fecha_mes = 12
    
update torneos 
set fecha_ano = 2022
where id_torneo in ('NHoIPMun4qEo5AfZrUT', 'NHPXlPzWLEPcjYzr96v', 'NHLaPErvfWlV76yUl-A', 'NHFU0VcGsME7zQNx3Ab', 'NH9FTjODm94nmVG-c-E',
'Nh76SJ8BsTm-6dHf5ff', 'Ngx-SviSXrnCAnXZ5td', 'NGWZLO8KFlCkofnCCZV', 'NGvh-HL9q61JxBgwiY0', 'NGRf-6HWX0bcuo9qw0R',
'NgOy0JxVdww43Zbb3Qp', 'NGmckRn3cYw6TnDJ890', 'NGGVtheTmEZ28vYzGvk', 'NGg327x-dt-y0PPUwuL', 'NFNVye7HW72pyS45dhP',
'NFnlh7NJs8eBg81tX51', 'NfjwABbGNzu3u2jQaec', 'NFhqFTWPSXUtnpAvNz8', 'NFE9-5T77Rl80FI6IRl', 'NeNdheBn2j-qOESBz3j',
'NdP-palS0e9I4cDsB4A')


create table partidos as
select *
from
    partidos_df
    
alter table partidos_v2 add primary key (id_torneo, categoria, nombre_partido)    
    
    
select 
    t.*,
    
from
    torneos
    
    
select 
    p.nombre_torneo,
    count(*) as qty
from
    partidos p
group by
    1
    



SELECT * FROM pg_stat_activity;
SELECT pg_terminate_backend(10955);



select *
from
    partidos p
where
    p.nombre_torneo = '1a Prueba Circuito Prinsotel 2024'

    
select 
    p.nombre_partido,
    max(p.pareja1) as pareja1,
    max(p.pareja2) as pareja1,
    max(p.pareja1_set1) as pareja1_set1,
    max(p.pareja1_set2) as pareja1_set2,
    max(p.pareja1_set3) as pareja1_set3,
    max(p.pareja2_set1) as pareja2_set1,
    max(p.pareja2_set2) as pareja2_set2,
    max(p.pareja2_set3) as pareja2_set3,
    max(p.pareja_ganadora) as pareja_ganadora,
    p.categoria,
    p.nombre_torneo 
from
    partidos_df_20230908 p
group by
    p.nombre_torneo, p.categoria, p.nombre_partido
    
    
    
    
select * 
from     
    jugadores
    
drop table jugadores

CREATE TABLE jugadores (
    id_jugador SERIAL PRIMARY KEY,
    nombre_jugador VARCHAR(255)
);
    
create table jugadores as

insert into jugadores(nombre_jugador)
(
select distinct nombre_jugador
from
(
with jugador as 
(
select    
    lower(trim(substring(p.pareja1 from 0 for position('-' in p.pareja1)))) as jugador1_pareja1,
    lower(trim(substring(p.pareja1 from position('-' in p.pareja1)+2 for length(p.pareja1)))) as jugador2_pareja1, 
    lower(trim(substring(p.pareja2 from 0 for position('-' in p.pareja2)))) as jugador1_pareja2,
    lower(trim(substring(p.pareja2 from position('-' in p.pareja2)+2 for length(p.pareja1)))) as jugador2_pareja2
from
    partidos p    
)    

select
    distinct a.jugador as nombre_jugador
from
    (-- a    
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


select *
from
    partidos p 
where
    p.nombre_torneo = 'Torneo Express Diciembre 5a Masculina'
    
    
    
insert into jugadores(nombre_jugador)
(
select distinct nombre_jugador
from
(
with jugador as
(
select
    lower(trim(substring(p.pareja1 from 0 for position('-' in p.pareja1)))) as jugador1_pareja1,
    lower(trim(substring(p.pareja1 from position('-' in p.pareja1)+2 for length(p.pareja1)))) as jugador2_pareja1,
    lower(trim(substring(p.pareja2 from 0 for position('-' in p.pareja2)))) as jugador1_pareja2,
    lower(trim(substring(p.pareja2 from position('-' in p.pareja2)+2 for length(p.pareja1)))) as jugador2_pareja2
from
    partidos p
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
);    


-- 
-- 

select 
    distinct t.id_torneo 
from 
    torneos t 
inner join
    partidos p
    on t.nombre_torneo = p.nombre_torneo 
where
    p.nombre_torneo is not null


ALTER TABLE torneos
ADD COLUMN status_scraping VARCHAR(255);


update torneos 
set status_scraping = 'procesado'
where nombre_torneo = 'Torneo Express Octubre'
and fecha_ano = '2023'
and lugar = 'Palma Padel'

where id_torneo in 
(select 
    distinct t.id_torneo 
from 
    torneos t 
inner join
    partidos p
    on t.nombre_torneo = p.nombre_torneo 
where
    p.nombre_torneo is not null)

    
truncate table  jugadores_unicos   
    
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
    and ju.nombre_jugador is null
    
    
CREATE TABLE jugadores_unicos (
    id_jugador_unico SERIAL PRIMARY KEY,
    nombre_jugador VARCHAR(255),
    nombre VARCHAR(255),
    apellido VARCHAR(255)
);    
    
CREATE TABLE union_jugadores (
    id_jugador_unico INT,
    id_jugador INT
);        

truncate table union_jugadores

alter table partidos_v2  add primary key (id_jugador_unico, id_jugador)  

select *
from
truncate table  jugadores_unicos
where
    apellido <> ''
    apellido = 'Jelenkiewicz'


select *
from
    partidos p 
where
    p.nombre_torneo = 'TORNEO EXPRESS 3B° CATEGORÍA EN SA CABANA'
    
    
--
--
select 
    j.nombre_jugador,
    j.nombre,
    j.apellido,
    p.fecha_ano,
    p.fecha_str,
    p.fecha_mes,
    p.lugar,
    p.nombre_torneo,
    p.categoria,
    p.nombre_partido,
    p.pareja1,
    p.pareja2,
    p.pareja_ganadora,
    count(distinct p.nombre_partido) as total_partidos_jugados,
    count(distinct 
        case when (j.nombre_jugador_var in (jugador1_pareja1, jugador2_pareja1) and p.pareja_ganadora = 'Pareja 1')
            or (j.nombre_jugador_var in (jugador1_pareja2, jugador2_pareja2) and p.pareja_ganadora = 'Pareja 2')
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
        ju.nombre_jugador,
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
        ju.id_jugador_unico = 26667
    )j   
inner join
    (-- p
    select 
        p.*,  
        t.lugar,
        t.fecha_str,
        t.fecha_ano,
        t.fecha_mes,
        lower(trim(substring(p.pareja1 from 0 for position('-' in p.pareja1)))) as jugador1_pareja1,
        lower(trim(substring(p.pareja1 from position('-' in p.pareja1)+2 for length(p.pareja1)))) as jugador2_pareja1, 
        lower(trim(substring(p.pareja2 from 0 for position('-' in p.pareja2)))) as jugador1_pareja2,
        lower(trim(substring(p.pareja2 from position('-' in p.pareja2)+2 for length(p.pareja1)))) as jugador2_pareja2
    from
        partidos p      
    inner join
        torneos t 
        on p.nombre_torneo = t.nombre_torneo
    )p
    on j.nombre_jugador_var in (p.jugador1_pareja1, jugador2_pareja1, jugador1_pareja2, jugador2_pareja2)    
group by
    1,2,3,4,5,6,7,8,9,10,11,12,13
    
    
    
-- 
-- 

select 
    j.nombre_jugador,    
    cast(p.fecha_ano as int)*100 + cast(p.fecha_mes as int) as month_id,
    p.fecha_str,    
    p.lugar,
    p.nombre_torneo,
    p.categoria,    
    count(distinct p.nombre_partido) as total_partidos_jugados,
    count(distinct 
        case when (j.nombre_jugador_var in (jugador1_pareja1, jugador2_pareja1) and p.pareja_ganadora = 'Pareja 1')
            or (j.nombre_jugador_var in (jugador1_pareja2, jugador2_pareja2) and p.pareja_ganadora = 'Pareja 2')
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
        ju.nombre_jugador,
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
        ju.id_jugador_unico = 26667
    )j   
inner join
    (-- p
    select 
        p.*,  
        t.lugar,
        t.fecha_str,
        t.fecha_ano,
        t.fecha_mes,
        lower(trim(substring(p.pareja1 from 0 for position('-' in p.pareja1)))) as jugador1_pareja1,
        lower(trim(substring(p.pareja1 from position('-' in p.pareja1)+2 for length(p.pareja1)))) as jugador2_pareja1, 
        lower(trim(substring(p.pareja2 from 0 for position('-' in p.pareja2)))) as jugador1_pareja2,
        lower(trim(substring(p.pareja2 from position('-' in p.pareja2)+2 for length(p.pareja1)))) as jugador2_pareja2
    from
        partidos p      
    inner join
        torneos t 
        on p.nombre_torneo = t.nombre_torneo
    )p
    on j.nombre_jugador_var in (p.jugador1_pareja1, jugador2_pareja1, jugador1_pareja2, jugador2_pareja2)    
group by
    1,2,3,4,5,6
order by
    2 asc
    
    
    
select *
from
    torneos
    
    
create table partidos_v2 as
(-- t
select 
    p.*,
    t.id_torneo,
    lower(trim(substring(p.pareja1 from 0 for position('-' in p.pareja1)))) as jugador1_pareja1,
    lower(trim(substring(p.pareja1 from position('-' in p.pareja1)+2 for length(p.pareja1)))) as jugador2_pareja1, 
    lower(trim(substring(p.pareja2 from 0 for position('-' in p.pareja2)))) as jugador1_pareja2,
    lower(trim(substring(p.pareja2 from position('-' in p.pareja2)+2 for length(p.pareja1)))) as jugador2_pareja2
from
    partidos p 
inner join
    torneos t 
    on p.nombre_torneo = t.nombre_torneo 
)