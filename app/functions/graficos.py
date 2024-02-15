import matplotlib
import re

matplotlib.use("TKAgg")
print(matplotlib.get_backend())

from matplotlib import pyplot as plt
import numpy as np

# Función para generar un gráfico y devolverlo en formato PNG
def generar_grafico(id_usuario):
    # Supongamos que tienes una función que genera el gráfico basado en el ID de usuario
    # Esto es solo un ejemplo, deberías reemplazarlo con tu lógica real
    plt.clf()
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title(f'Gráfico del usuario {id_usuario}')


    # Devolver el buffer de imagen como un archivo PNG
    return plt


def bar_graph( eje_x, valores_y, orientacion_barras='vertical'):
    #plt.clf()

    fig, ax = plt.subplots(figsize=(2.1, 5))
    # Configurar el color de fondo del gráfico y su transparencia
    fig.patch.set_facecolor('none')  # 'none' para hacer el fondo transparente
    fig.patch.set_alpha(0)  # Configurar la transparencia (0 para completamente transparente, 1 para opaco)

    width = 0.2  # Ancho de las barras

    # Definir colores personalizados para las barras
    color_verde_claro = '#b7e4c7'  # Puedes usar códigos hexadecimales
    color_lila_claro = '#d9b3ff'

    # Definir la ubicación de las etiquetas de datos
    etiquetas_x = np.arange(len(eje_x))

    # Inicializar bottom como un array de ceros
    bottom = np.zeros(len(eje_x))

    # Extraer las claves y valores del diccionario
    claves = list(valores_y.keys())
    valores = list(valores_y.values())

    if orientacion_barras == 'vertical':

        # Barra principal (Torneos jugados)
        p1 = ax.bar(eje_x, valores[0], width, bottom=bottom, label=claves[0], color=color_lila_claro)

        # Barra secundaria (Torneos ganados)
        p2 = ax.bar(eje_x, valores[1], width, bottom=bottom, label=claves[1], color=color_verde_claro)

        # Añadir etiquetas de datos
        for idx, val in enumerate(valores[0]):
            sub_bar_val = valores[1][idx]  # Valor de la barra secundaria en la misma posición
            ax.text(etiquetas_x[idx], val + 0.1, f'Jugados: {val}\nGanados: {sub_bar_val}', ha='center', color='gray',
                    fontsize=7)

        # Cambiar el color de la línea del eje X a gris
        ax.xaxis.label.set_color('gray')
        # Girar las etiquetas del eje X verticalmente con una ligera inclinación
        ax.tick_params(axis='x',  bottom=False, labelrotation=45, colors='#4a524d', size=9)
        # Ocultar las etiquetas del eje Y
        ax.tick_params(axis='y', which='both', left=False)
        ax.yaxis.set_visible(False)
        fig.subplots_adjust(top=0.95, bottom=0.1, left=0.05, right=0.95)


    elif orientacion_barras == 'horizontal':

        # Barra principal (Torneos jugados)
        p1 = ax.barh(eje_x, valores[0], height=width, left=0, label=claves[0], color=color_lila_claro)

        # Barra secundaria (Torneos ganados)
        p2 = ax.barh(eje_x, valores[1], height=width, left=0, label=claves[1], color=color_verde_claro)

        # Añadir etiquetas de datos
        for idx, val in enumerate(valores[0]):
            sub_bar_val = valores[1][idx]  # Valor de la barra secundaria en la misma posición
            ax.text(val +0.1,
                    etiquetas_x[idx],
                    f'J: {val}\nG: {sub_bar_val}',
                    va='center',
                    color='gray',
                    fontsize=7,
                    fontweight='bold')


        # Cambiar el color de la línea del eje Y a gris
        ax.yaxis.label.set_color('gray')
        ax.tick_params(axis='y', left=False, colors='#4a524d')

        # Dividir etiquetas del eje Y en dos líneas si el texto es demasiado largo
        ax.set_yticklabels([re.sub(r'(\w+)(\s+)', r'\1\n\2', cat) for cat in eje_x], ha='right', fontsize=9)
        ax.xaxis.set_visible(False)
        fig.subplots_adjust(top=0.97, bottom=0.03, left=0.35, right=0.9)

    # Ocultar los bordes de la gráfica
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)


    return fig

