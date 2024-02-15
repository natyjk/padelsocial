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

load_dotenv()

class Torneo:
    def __init__(self, id_torneo):

        self.id_torneo = id_torneo
        self.obtener_data_torneo()

    def obtener_data_torneo(self):
        db = Database()
        dict_torneo = db.get_info_torneo(self.id_torneo)
        self.nombre_torneo = dict_torneo['nombre_torneo']
        self.lugar = dict_torneo['lugar']
        self.fecha_ano = dict_torneo['fecha_ano']
        self.fecha_mes = dict_torneo['fecha_mes']
        self.fecha_str = dict_torneo['fecha_str']
        self.fecha = pd.to_datetime(f"{dict_torneo['fecha_ano']}-{dict_torneo['fecha_mes']}", format="%Y-%m")
        self.link = 'https://torneos.sportelia.es/#/tournaments-details/-{0}/%3Aembed'.format(self.id_torneo)

    def scrapear_cuadro(self):
        partidos_all = pd.DataFrame()
        # Inicializar el controlador de Selenium
        driver = webdriver.Chrome()
        # Abrir la página web
        driver.get(self.link)
        # Esperar a que se cargue la página
        wait = WebDriverWait(driver, 30)
        time.sleep(3)

        # Busca las categorías del torneo
        cats = driver.find_elements(By.CSS_SELECTOR, 'ion-item-group')

        for c2 in cats:
            categorias = c2.find_elements(By.CSS_SELECTOR, 'ion-item.item')

            for c in categorias:
                try:
                    nombre_categoria = c.find_elements(By.TAG_NAME, 'h2')
                    nombre_categoria_tx = nombre_categoria[0].text

                    # Hace click en el elemento de la categoria
                    nombre_categoria[0].click()
                    time.sleep(2)
                    # Esperar a que se cargue la página
                    wait = WebDriverWait(driver, 30)

                    ini = driver.find_elements(By.TAG_NAME, 'ion-navbar')

                    # Si se abre la ventana de iniciar sesión la cierra y sigue
                    for i in ini:
                        if i.text == 'Iniciar sesión':
                            close_button = i.find_elements(By.CSS_SELECTOR, 'button')
                            for i in close_button:
                                atr = i.get_attribute('class')
                                if atr == 'bar-button bar-button-md bar-button-default bar-button-default-md':
                                    i.click()

                    df = self.extraer_desde_categoria(driver)

                    df['categoria'] = nombre_categoria_tx
                    df['nombre_torneo'] = self.nombre_torneo
                    df['id_torneo'] = self.id_torneo
                    df[['jugador1_pareja1', 'jugador2_pareja1']] = df['pareja1'].str.split('-', expand=True)
                    # Limpiar y convertir a minúsculas
                    df['jugador1_pareja1'] = df['jugador1_pareja1'].str.strip().str.lower()
                    df['jugador2_pareja1'] = df['jugador2_pareja1'].str.strip().str.lower()

                    df[['jugador1_pareja2', 'jugador2_pareja2']] = df['pareja2'].str.split('-', expand=True)
                    df['jugador1_pareja2'] = df['jugador1_pareja2'].str.strip().str.lower()
                    df['jugador2_pareja2'] = df['jugador2_pareja2'].str.strip().str.lower()

                    partidos_all = pd.concat([partidos_all, df])

                except:
                    continue


        return partidos_all

    def extraer_desde_categoria(self, driver):
        partidos_df = pd.DataFrame()
        # Hace click en el elemento de la categoria
        time.sleep(2)
        # Esperar a que se cargue la página
        wait = WebDriverWait(driver, 30)

        # Obtener el HTML de la página (donde está el driver -_> navegador abierto)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")  # pone el código más bonito

        partidos = driver.find_elements(By.CSS_SELECTOR, 'ion-card.score-card')

        for p in partidos:

            datos_partido = p.find_elements(By.CSS_SELECTOR, 'button.item')
            nombre_partido = datos_partido[0].text
            pareja1 = datos_partido[1].find_elements(By.TAG_NAME, 'h2')
            pareja1 = pareja1[0].text

            pareja1_win = False
            p1w = datos_partido[1].find_elements(By.CSS_SELECTOR, 'ion-icon')

            if len(p1w) > 0:
                variable1 = p1w[0].get_attribute('aria-label')

                if variable1 == 'trophy':
                    pareja1_win = True

            sets_1 = datos_partido[1].find_elements(By.TAG_NAME, 'button')

            n_sets_1 = len(sets_1)

            if n_sets_1 > 0:

                try:
                    pareja1_set1 = sets_1[0].text
                    pareja1_set2 = sets_1[1].text

                    if n_sets_1 == 3:
                        pareja1_set3 = sets_1[2].text
                    else:
                        pareja1_set3 = 0

                except(IndexError, AttributeError):
                    pareja1_set1 = 0
                    pareja1_set2 = 0
                    pareja1_set3 = 0

            pareja2 = datos_partido[2].find_elements(By.TAG_NAME, 'h2')
            pareja2 = pareja2[0].text

            pareja2_win = False
            p2w = datos_partido[2].find_elements(By.CSS_SELECTOR, 'ion-icon')

            if len(p2w) > 0:
                variable2 = p2w[0].get_attribute('aria-label')

                if variable2 == 'trophy':
                    pareja2_win = True

            sets_2 = datos_partido[2].find_elements(By.TAG_NAME, 'button')

            n_sets_2 = len(sets_2)
            if n_sets_2 > 0:
                try:
                    pareja2_set1 = sets_2[0].text
                    pareja2_set2 = sets_2[1].text

                    if n_sets_2 == 3:
                        pareja2_set3 = sets_2[2].text
                    else:
                        pareja2_set3 = 0

                except(IndexError, AttributeError):
                    pareja2_set1 = 0
                    pareja2_set2 = 0
                    pareja2_set3 = 0

            if pareja1_win:
                pareja_ganadora = 'Pareja 1'
            elif pareja2_win:
                pareja_ganadora = 'Pareja 2'
            else:
                pareja_ganadora = 'NN'

            if 'pareja1_set1' in locals():
                pareja1_set1_ = pareja1_set1
            else:
                pareja1_set1_ = 0

            if 'pareja1_set2' in locals():
                pareja1_set2_ = pareja1_set2
            else:
                pareja1_set2_ = 0

            if 'pareja1_set3' in locals():
                pareja1_set3_ = pareja1_set3
            else:
                pareja1_set3_ = 0

            if 'pareja2_set1' in locals():
                pareja2_set1_ = pareja2_set1
            else:
                pareja2_set1_ = 0

            if 'pareja2_set2' in locals():
                pareja2_set2_ = pareja1_set2
            else:
                pareja2_set2_ = 0

            if 'pareja2_set3' in locals():
                pareja2_set3_ = pareja2_set3
            else:
                pareja2_set3_ = 0

            row = {'nombre_partido': nombre_partido,
                   'pareja1': pareja1,
                   'pareja2': pareja2,
                   'pareja1_set1': pareja1_set1_,
                   'pareja1_set2': pareja1_set2_,
                   'pareja1_set3': pareja1_set3_,
                   'pareja2_set1': pareja2_set1_,
                   'pareja2_set2': pareja2_set2_,
                   'pareja2_set3': pareja2_set3_,
                   'pareja_ganadora': pareja_ganadora
                   }

            # print(row)
            # partidos_df = partidos_df.append(row, ignore_index=True)

            row_df = pd.DataFrame([row])
            partidos_df = pd.concat([partidos_df, row_df], ignore_index=True)

        driver.back()

        return partidos_df

