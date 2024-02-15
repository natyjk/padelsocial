
from flask import Flask, render_template, redirect, url_for, request, jsonify, send_file
from functions.database import Database
from functions.torneos import Torneo
from functions.jugador import Jugador
from functions import helpers as hp
from functions import graficos as gr
import json
from collections import OrderedDict
from multiprocessing import Process
import base64
from io import BytesIO
app = Flask(__name__)


@app.before_request
def before_request():
    print('Antes de la petición...')


@app.after_request
def after_request(response):
    print('Después de la petición')
    return response


@app.route("/")
def index():
    return render_template('index2.html')


@app.route('/procesar', methods=['POST'])
def menu_inicio():
    opcion_seleccionada = request.form['opcion']
    return redirect(url_for(hp.opciones_home(opcion_seleccionada)))


@app.route("/torneos", methods=["GET", "POST"])
def torneos_cargados():

    torneos_html = hp.cargar_torneos()
    return render_template('torneos.html', torneos_html=torneos_html)


@app.route("/torneos_procesar", methods=["GET", "POST"])
def torneos_procesar():
    return render_template('torneos_procesar.html')


@app.route("/jugadores_admin", methods=["GET", "POST"])
def revisar_jugadores():
    return render_template('jugadores_admin.html')

@app.route("/resultados_persona", methods=["GET", "POST"])
def resultados_persona():
    return render_template('datos_usuario.html')

@app.route("/metricas_usuario", methods=["GET", "POST"])
def metricas_usuario():
    return render_template('metricas_usuario.html')


@app.route('/extraer_data_torneo/<string:torneo_id>', methods=['GET'])
def extraer_data_torneo(torneo_id):
    resultado = hp.scrapear_torneo(torneo_id)
    return jsonify(resultado)


@app.route('/scrapear_torneos', methods=['POST'])
def scrapea_torneos():
    datos = request.json
    lista_torneos = datos['torneo_id']
    for id_torneo in lista_torneos:
        try:
            resultado = hp.scrapear_torneo(id_torneo)
        except Exception as e:
            print('Error procesar torneo - Error: {}'.format(e))
            raise e

        # Haz algo con el resultado si es necesario
    return jsonify(resultado)

@app.route('/cargar_nombres/<string:texto_buscado>', methods=['GET'])
def cargar_nombres(texto_buscado):
    db = Database()
    jugadores_all = db.select_jugadores(texto_buscado)
    jugadores_all = jugadores_all.to_dict(orient='records')

    jugadores_unicos = db.select_jugadores_unicos(texto_buscado)
    jugadores_unicos = jugadores_unicos.to_dict(orient='records')

    data = {'jugadores_all': jugadores_all, 'jugadores_unicos': jugadores_unicos}

    return jsonify(data)


@app.route('/agrupar_jugadores/', methods=['POST'])
def agrupar_jugadores():
    data = request.get_json()
    lista_izquierda = json.loads(data['nombresIzquierda'])
    nombre_derecha = data['nombreDerecha']
    hp.agrupar_jugadores(lista_izquierda, nombre_completo=nombre_derecha)

    return jsonify({'mensaje': 'Agrupar jugadores procesado'})


@app.route('/actualizar_jugadores', methods=['GET'])
def actualizar_jugadores():
    db = Database()
    db.actualizar_jugadores()

    return jsonify({'mensaje': 'Tabla jugadores actualizada'})

@app.route('/crear_nuevo_jugador/', methods=['POST'])
def crear_nuevo_jugador():
    data = request.get_json()
    print(data)

    lista_izquierda = data['nombresIzquierda']
    nombre = data['nombre']
    apellido = data['apellido']
    db = Database()
    id_jugador_unico = db.crear_jugador_unico(nombre, apellido)
    print('ID JUGADOR UNICO CREADO: {}'.format(id_jugador_unico))
    hp.agrupar_jugadores(lista_izquierda, id_jugador_unico=id_jugador_unico)


    return jsonify({'mensaje': 'Tabla jugadores únicos actualizado nombre y apellido!'})

@app.route('/obtener_lista_jugadores')
def obtener_lista_jugadores():
    db = Database()
    lista_jugadores = db.obtener_lista_jugadores()
    lista_jugadores = lista_jugadores[['id_jugador_unico', 'nombre_completo']]
    lista_jugadores = lista_jugadores.to_dict(orient='records')

    return jsonify(lista_jugadores)

@app.route('/obtener_lista_torneos')
def obtener_lista_torneos():
    db = Database()
    lista_torneos = db.get_torneos_data()
    lista_torneos['status_scraping'] = lista_torneos['status_scraping'].fillna('None')
    lista_torneos = lista_torneos.to_dict(orient='records')

    return jsonify(lista_torneos)

# obtener_lista_torneos

@app.route('/obtener_torneos_jugador/<id_usuario_unico>')
def obtener_torneos_jugador(id_usuario_unico):

    jugador = Jugador(id_usuario_unico)
    all_torneos_jugador = jugador.obtener_torneos_jugador()
    all_torneos_jugador = all_torneos_jugador.to_dict(orient='list')

    return jsonify(all_torneos_jugador)


@app.route('/cargar_datos_usuario/<id_usuario_unico>')
def cargar_datos_usuario(id_usuario_unico):

    jugador = Jugador(id_usuario_unico)
    data_principal_jugador = jugador.obtener_data_jugador()

    #data_principal_jugador = data_principal_jugador.to_dict(orient='list')
    print(data_principal_jugador)

    return jsonify(data_principal_jugador)

# Ruta en Flask para generar y devolver el gráfico
@app.route('/grafico/<id_usuario_unico>')
def obtener_grafico(id_usuario_unico):
    jugador = Jugador(id_usuario_unico)
    graficos = jugador.crear_graficos_generales()

    # Devolver las imágenes Base64 como una lista JSON
    return jsonify(graficos)




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=9999)


