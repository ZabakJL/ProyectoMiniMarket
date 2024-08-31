# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 18:26:10 2024

@author: jpmog
"""

# Importar bibliotecas y funciones 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd

# Definir una paleta de colores
colores1 = plt.cm.tab20(np.linspace(0, 1, 20))
colores2 = plt.cm.tab20b(np.linspace(0, 1, 20))
colores_combinados = np.vstack((colores1, colores2))
colores = colores_combinados[::2][:20]
colores


def drawBoxes (datos, var_interes, value_vars, x, cols, colores=colores):
    """
    Recibe un dataframe, una lista de variables de interes, una lista de variables de valores, una cadena
    que identifica el nombre de la columna por el que se diviran las series en el eje x, 
    un número de columnas para las gráficas, y una lista de colores. 

    La función dibuja una gráfica de boxplot para las series indicadas en X, y presenta en columnas las variables de interes 

    """
    melted = pd.melt(datos, id_vars=var_interes, value_vars=value_vars, var_name='Grupo', value_name='Valor')
    g = sns.catplot(col='Grupo', x=x, y='Valor', col_wrap=cols, kind='box', data=melted, sharey=False, palette=colores, showmeans=True)