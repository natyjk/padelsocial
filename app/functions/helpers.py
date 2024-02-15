import pandas as pd
from dotenv import load_dotenv
import os
from os import environ
from functions.database import Database
from functions.torneos import Torneo

load_dotenv()


def opciones_home(opcion_seleccionada):

    if opcion_seleccionada == 'torneos_cargados':
        url_to = 'torneos_cargados'
    elif opcion_seleccionada == 'resultados_persona':
        url_to = 'metricas_usuario'
    elif opcion_seleccionada == 'metricas_generales':
        url_to = 'metricas_generales'
    elif opcion_seleccionada == 'revisar_jugadores':
        url_to = 'revisar_jugadores'
    else:
        # Manejar opciones no esperadas
        url_to ='index'

    return url_to


# Función para generar el HTML de los enlaces
def generar_enlace(row):
    if pd.isnull(row['status_scraping']):
        link_to = f'<a href="#" class="extraer-data-torneo" data-id="{row["id_torneo"]}">Extraer Data</a>'
    else:
            link_to = ''
    return link_to


def scrapear_torneo(torneo_id):
    torneo = Torneo(torneo_id)
    partidos = torneo.scrapear_cuadro()

    db = Database()

    if len(partidos) > 0:
        print(partidos)
        db.guardar_partidos(partidos)
        db.update_status_scraping_torneo(torneo_id, 'procesado')

    else:
        db.update_status_scraping_torneo(torneo_id, 'procesado - sin data')

    resultado = {'mensaje': 'Partidos guardados del torneo: {}'.format(torneo.nombre_torneo)}

    return resultado


def cargar_torneos():
    db = Database()
    torneos = db.get_torneos_data()
    url_torneos = 'https://torneos.sportelia.es/#/tournaments-details/-'
    torneos['nombre_torneo'] = torneos.apply(
        lambda row: f'<a href="{url_torneos}{row["id_torneo"]}/%3Aembed">{row["nombre_torneo"]}</a>', axis=1)

    torneos['accion'] = torneos.apply(generar_enlace, axis=1)

    torneos = torneos[['fecha_ano', 'fecha_str', 'nombre_torneo', 'lugar', 'partidos', 'status_scraping', 'accion']]
    torneos_html = torneos.to_html(classes='table table-striped', index=False, escape=False)

    return torneos_html


def agrupar_jugadores(lista_jugadores, id_jugador_unico=0, nombre_completo=''):
    db = Database()
    if id_jugador_unico == 0:
        id_jugador_unico = db.get_id_jugador_unico(nombre_completo)

    jugadores = pd.DataFrame(lista_jugadores, columns=['nombre_jugador'])

    jugadores['id_jugador'] = jugadores['nombre_jugador'].apply(db.get_id_jugador)
    jugadores['id_jugador_unico'] = id_jugador_unico

    jugadores = jugadores[['id_jugador', 'id_jugador_unico']]
    print(jugadores)

    db.insertar_registro_union_jugadores(jugadores)
    #db.eliminar_jugadores_unicos(lista_jugadores, jugador_unico)

    print('Agrupar Jugadores procesado!')

    return jugadores