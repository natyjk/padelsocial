from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

from dotenv import load_dotenv
from os import environ
from functions.database import Database
from functions import graficos as gr
import base64
from io import BytesIO

load_dotenv()

class Jugador:
    def __init__(self, id_jugador_unico):

        self.id_jugador_unico = id_jugador_unico
        self.obtener_data_jugador()

    def obtener_data_jugador(self):
        db = Database()
        dict_jugador = db.get_data_jugador(self.id_jugador_unico)
        self.nombre_completo = dict_jugador['nombre_completo']
        self.nombre = dict_jugador['nombre']
        self.apellido = dict_jugador['apellido']
        self.torneos_jugados = dict_jugador['torneos_jugados']
        self.categorias_jugadas = dict_jugador['categorias_jugadas']
        self.total_partidos_jugados = dict_jugador['total_partidos_jugados']
        self.partidos_ganados = dict_jugador['partidos_ganados']
        self.finales_jugadas = dict_jugador['finales_jugadas']
        self.finales_ganadas = dict_jugador['finales_ganadas']


        dict_jugador['p_partidos_ganados'] = dict_jugador['partidos_ganados'] / dict_jugador['total_partidos_jugados']
        dict_jugador['p_torneos_ganados'] = dict_jugador['finales_ganadas'] / dict_jugador['torneos_jugados']
        dict_jugador['p_finales'] = dict_jugador['finales_jugadas'] / dict_jugador['torneos_jugados']

        return dict_jugador


    def obtener_all_data_jugador(self):
        db = Database()
        df = db.get_all_data_jugador(self.id_jugador_unico)

        return df

    def obtener_torneos_jugador(self):
        db = Database()
        df = db.get_torneos_jugador(self.id_jugador_unico)

        return df

    def crear_graficos_generales(self):

        df_stats_year = self.df_stats_grouped('fecha_ano')
        eje_x_years = df_stats_year['fecha_ano'].tolist()
        valores_y = {
            'Torneos jugados': df_stats_year['torneos_jugados'].tolist(),
            'Torneos ganados': df_stats_year['torneos_ganados'].tolist()
        }

        graph1 = gr.bar_graph(eje_x_years, valores_y)
        buffer1 = BytesIO()
        graph1.savefig(buffer1, format='png',transparent=True)
        buffer1.seek(0)
        graph1_base64 = base64.b64encode(buffer1.read()).decode('utf-8')

        df_stats_category = self.df_stats_grouped('categoria')
        df_stats_category = df_stats_category.sort_values(by=['torneos_jugados','torneos_ganados'], ascending=False, ignore_index=True)
        df_stats_category = df_stats_category[::-1]
        eje_x_category = df_stats_category['categoria'].tolist()
        valores_y = {
            'Torneos jugados': df_stats_category['torneos_jugados'].tolist(),
            'Torneos ganados': df_stats_category['torneos_ganados'].tolist()
        }

        graph2 = gr.bar_graph(eje_x_category, valores_y, 'horizontal')
        buffer2 = BytesIO()
        graph2.savefig(buffer2, format='png',transparent=True)
        buffer2.seek(0)
        graph2_base64 = base64.b64encode(buffer2.read()).decode('utf-8')

        df_stats_club = self.df_stats_grouped('lugar')
        df_stats_club = df_stats_club.sort_values(by=['torneos_jugados','torneos_ganados'], ascending=False, ignore_index=True)

        df_stats_club = df_stats_club.head(8)
        df_stats_club = df_stats_club[::-1]

        eje_x_category = df_stats_club['lugar'].tolist()
        valores_y = {
            'Torneos jugados': df_stats_club['torneos_jugados'].tolist(),
            'Torneos ganados': df_stats_club['torneos_ganados'].tolist()
        }

        graph3 = gr.bar_graph(eje_x_category, valores_y, 'horizontal')
        buffer3 = BytesIO()
        graph3.savefig(buffer3, format='png',transparent=True)
        buffer3.seek(0)
        graph3_base64 = base64.b64encode(buffer3.read()).decode('utf-8')



        df_stats_pareja = self.df_stats_grouped('pareja')

        df_stats_pareja = df_stats_pareja.sort_values(by=['torneos_jugados','torneos_ganados'], ascending=False, ignore_index=True)
        df_stats_pareja = df_stats_pareja.head(8)
        df_stats_pareja = df_stats_pareja[::-1]
        eje_x_pareja = df_stats_pareja['pareja'].tolist()
        valores_y = {
            'Torneos jugados': df_stats_pareja['torneos_jugados'].tolist(),
            'Torneos ganados': df_stats_pareja['torneos_ganados'].tolist()
        }

        graph4 = gr.bar_graph(eje_x_pareja, valores_y, 'horizontal')
        buffer4 = BytesIO()
        graph4.savefig(buffer4, format='png', transparent=True)
        buffer4.seek(0)
        graph4_base64 = base64.b64encode(buffer4.read()).decode('utf-8')

        graficos = {'graph1': graph1_base64, 'graph2': graph2_base64, 'graph3': graph3_base64, 'graph4': graph4_base64}

        return graficos

    def df_stats_grouped(self, grouped):
        df = self.obtener_all_data_jugador()

        # Definir las funciones de agregación deseadas
        aggregation_functions = {
            'id_torneo': 'nunique',
            'finales_ganadas': 'sum'
        }

        # Aplicar las funciones de agregación
        df_agrupado = df.groupby([grouped]).agg(aggregation_functions)

        # Renombrar las columnas resultantes si es necesario
        df_agrupado = df_agrupado.rename(columns={'id_torneo': 'torneos_jugados',
                                                  'finales_ganadas': 'torneos_ganados'})

        # Para reajustar el índice y obtener un DataFrame plano, puedes hacer lo siguiente:
        df_agrupado = df_agrupado.reset_index()

        return df_agrupado


