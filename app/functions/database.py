import pandas as pd
from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.sql import text
from config.settings import config_bbdd
from dotenv import load_dotenv
import os
from os import environ
import unicodedata


load_dotenv()

class Database:
    def __init__(self,
            host=config_bbdd['host'],
            database=config_bbdd['database'],
            port=config_bbdd['port'],
            user=config_bbdd['user'],
            password=config_bbdd['pass']):

        str_conn = 'postgresql://{0}:@{1}:{2}/{3}'.format(
            user, host, port, database
        )

        self.connection = create_engine(str_conn)

    def get_torneos_data(self):
        sql = """select 
                    t.*,
                    count(p.*) as partidos
                from
                    torneos t
                left join
                    partidos_v2 p
                    on p.id_torneo = t.id_torneo
                group by
                    t.id_torneo
                order by 
                    t.fecha_ano asc, t.fecha_mes desc, t.id_torneo desc;"""
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e
        return df

    def get_info_torneo(self, id_torneo):
        sql = """select 
                    *
                from
                    torneos t
                where 
                    t.id_torneo = '{}';""".format(id_torneo)
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e

        dict_torneo = df.iloc[0].to_dict()
        return dict_torneo

    def guardar_partidos(self, df):
        # Insertar o actualizar datos en la tabla 'nombre_tabla' desde el DataFrame 'torneos_df'
        df.to_sql('partidos_v2', con=self.connection, if_exists='append', index=False, method='multi', chunksize=5000)

    def actualizar_jugadores(self):

        nombre_query='actualizar_jugadores'
        sql = open('{0}sportelia/app/static/sql/{1}.sql'.format(environ.get('PROJECT_PATH'), nombre_query), 'r')
        sql = sql.read()

        nombre_query2 = 'insert_into_jugadores_unicos'
        sql2 = open('{0}sportelia/app/static/sql/{1}.sql'.format(environ.get('PROJECT_PATH'), nombre_query2), 'r')
        sql2 = sql2.read()

        with self.connection.connect() as conn:
            result = conn.execute(text(sql))
            conn.commit()
            result = conn.execute(text(sql2))
            conn.commit()
            conn.close()

            print('Ejecuto query actualizar users')


        return result

    def update_status_scraping_torneo(self, id_torneo, status):

        sql = """UPDATE torneos SET status_scraping = '{0}' WHERE  id_torneo = '{1}' ;""".format(status, id_torneo)

        with self.connection.connect() as conn:
            result = conn.execute(text(sql))
            conn.commit()
            conn.close()

            print('Update status scraping torneo')

        return result

    def select_jugadores(self, texto_buscado):
        sql = """SELECT j.* 
                FROM jugadores j
                LEFT JOIN union_jugadores ju
                    ON j.id_jugador = ju.id_jugador
                WHERE 
                    j.nombre_jugador LIKE '%{0}%'
                    AND ju.id_jugador IS NULL
                ORDER BY
                    j.nombre_jugador ASC;""".format(texto_buscado)
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e
        return df

    def select_jugadores_unicos(self, texto_buscado):
        sql = """SELECT * FROM jugadores_unicos WHERE LOWER(nombre_completo) LIKE '%{0}%'
                ORDER BY nombre_completo DESC;""".format(texto_buscado)
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e
        return df

    def get_id_jugador(self, nombre_jugador):
        sql = """select 
                    t.id_jugador
                from
                    jugadores t
                where 
                    t.nombre_jugador = '{}';""".format(nombre_jugador)
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e

        id_jugador = df.iloc[0]

        return id_jugador

    def get_id_jugador_unico(self, nombre_completo):
        sql = """select 
                    t.id_jugador_unico
                from
                    jugadores_unicos t
                where 
                    t.nombre_completo = '{}';""".format(nombre_completo)
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e

        id_jugador_unico = df['id_jugador_unico'].iloc[0]

        return id_jugador_unico

    def insertar_registro_union_jugadores(self, df):

        df.to_sql('union_jugadores', con=self.connection, if_exists='append', index=False, method='multi', chunksize=5000)
        print('Datos insertados en jugadores únicos')

    def eliminar_jugadores_unicos(self, lista_nombres, nombre_unico):

        # Eliminar todas las apariciones de 'nombre_unico'
        lista_nombres = [nombre for nombre in lista_nombres if nombre != nombre_unico]

        if len(lista_nombres) > 0:

            string_nombres = ", ".join([f"'{nombre}'" for nombre in lista_nombres])

            sql = """DELETE FROM jugadores_unicos WHERE nombre_jugador IN ({0}) ;""".format(string_nombres)

            with self.connection.connect() as conn:
                result = conn.execute(text(sql))
                conn.commit()
                conn.close()

                print('Usuarios replicados eliminados')

    def update_nombre_jugador(self, nombre_jugador, nombre, apellido):

        sql = """UPDATE jugadores_unicos
                SET nombre = '{0}',
                    apellido= '{1}'
                WHERE nombre_jugador = '{2}'""".format( nombre, apellido, nombre_jugador)

        with self.connection.connect() as conn:
            result = conn.execute(text(sql))
            conn.commit()
            conn.close()

        return result

    def obtener_lista_jugadores(self):
        sql = """select ju.*
                from
                    jugadores_unicos ju                 
                order by
                    ju.nombre_completo asc;"""
        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e

        return df

    def get_data_jugador(self, id_jugador_unico):
        nombre_query = 'select_data_general_jugador'
        sql = open('{0}sportelia/app/static/sql/{1}.sql'.format(environ.get('PROJECT_PATH'), nombre_query), 'r')
        sql = sql.read().format(id_jugador_unico)

        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e

        dict_jugador = df.iloc[0].to_dict()
        return dict_jugador

    def get_all_data_jugador(self, id_jugador_unico):
        nombre_query = 'select_all_data_jugador'
        sql = open('{0}sportelia/app/static/sql/{1}.sql'.format(environ.get('PROJECT_PATH'), nombre_query), 'r')
        sql = sql.read().format(id_jugador_unico)

        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e


        return df

    def get_torneos_jugador(self, id_jugador_unico):
        nombre_query = 'select_torneos_jugador'
        sql = open('{0}sportelia/app/static/sql/{1}.sql'.format(environ.get('PROJECT_PATH'), nombre_query), 'r')
        sql = sql.read().format(id_jugador_unico)

        try:
            df = pd.read_sql_query(con=self.connection.connect(),
                                   sql=sql_text(sql))

        except Exception as e:
            raise e

        return df

    def crear_jugador_unico(self, nombre, apellido):

        # Eliminar los acentos y convertir a minúsculas
        nombre_editado = ''.join(
            c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn').lower()
        apellido_editado = ''.join(
            c for c in unicodedata.normalize('NFD', apellido) if unicodedata.category(c) != 'Mn').lower()

        # Reemplazar los espacios con nada (quitarlos)
        nombre_editado = nombre_editado.replace(" ", "")
        apellido_editado = apellido_editado.replace(" ", "")

        nombre_completo_limpio = nombre_editado + apellido_editado
        nombre_completo = '{0} {1}'.format(nombre, apellido)
        sql = """INSERT INTO jugadores_unicos (nombre, apellido, nombre_completo, nombre_completo_limpio) 
                VALUES('{0}','{1}','{2}','{3}')
                RETURNING id_jugador_unico""".format(nombre, apellido, nombre_completo, nombre_completo_limpio)

        with self.connection.connect() as conn:
            result = conn.execute(text(sql))
            print('AQUIIIII')
            print(result)
            id_jugador_unico = result.fetchone()[0]
            conn.commit()
            conn.close()

        return id_jugador_unico

