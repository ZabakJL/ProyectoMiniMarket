

# Importar bibliotecas y funciones 
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import string


# Definir una paleta de colores
colores1 = plt.cm.tab20(np.linspace(0, 1, 20))
colores2 = plt.cm.tab20b(np.linspace(0, 1, 20))
colores_combinados = np.vstack((colores1, colores2))
colores = colores_combinados[::2][:20]
colores
cmap_personalizado = mcolors.ListedColormap(colores_combinados)

def graficar_boxplots(df, cols, num_col=3, ancho=15, alto_fila=5, titulo=None, colores=colores_combinados):
    """
    Genera una grilla de gráficos de boxplot para las columnas especificadas de un DataFrame.

    Parámetros:
    df (DataFrame): El DataFrame que contiene los datos.
    cols (list): Lista de nombres de columnas del DataFrame para las cuales se generarán los boxplots.
    num_col (int): Número de columnas en la grilla de gráficos. Valor por defecto es 3.
    ancho (int): Ancho total de la figura. Valor por defecto es 15.
    alto_fila (int): Alto de cada fila en la grilla. Valor por defecto es 5.
    titulo (str): Título opcional para la figura. Si no se proporciona, no se imprimirá ningún título.
    colores (list): Lista opcional de colores para los boxplots. Si no se proporciona, se usarán los colores por defecto.

    Descripción:
    - La función crea una grilla de gráficos de boxplot, donde cada gráfico corresponde a una de las columnas 
      especificadas en `cols`.
    - Cada gráfico de boxplot muestra el promedio (en rojo), así como los valores de Q1 (percentil 25), 
      Q2 (mediana), Q3 (percentil 75), mínimo y máximo, con etiquetas junto al eje y.
    - El número de filas en la grilla se calcula automáticamente en función de la cantidad de columnas y 
      el parámetro `num_col`.
    - La altura total de la figura se calcula como `alto_fila` multiplicado por el número de filas en la grilla.
    - Si se proporciona un `titulo`, se imprime como título general de la figura.
    - Si se proporciona una lista de `colores`, estos se aplicarán a los boxplots en el mismo orden.
    
    Retorno:
    fig (Figure): La figura creada que contiene la grilla de boxplots.

    """
    num_cols = len(cols)
    num_filas = -(-num_cols // num_col)  # Redondeo hacia arriba
    alto = num_filas * alto_fila
    
    fig, axes = plt.subplots(num_filas, num_col, figsize=(ancho, alto), squeeze=False)
    axes = axes.flatten()
    
    for i, col in enumerate(cols):
        if col in df.columns:
            # Definir color del boxplot
            color = colores[i] if colores is not None and len(colores) > 0 and i < len(colores) else None
            
            # Crear el boxplot
            bp = df.boxplot(column=col, ax=axes[i], showmeans=True, patch_artist=True,
                            boxprops=dict(facecolor=color))
            
            # Obtener estadísticas
            stats = df[col].describe()
            q1 = stats['25%']
            q2 = stats['50%']
            q3 = stats['75%']
            min_val = stats['min']
            max_val = stats['max']
            mean_val = stats['mean']
            
            # Agregar texto con estadísticas
            axes[i].text(1.1, q1, f'Q1: {q1:.2f}', va='center', ha='left', size=6)
            axes[i].text(1.1, q2, f'Q2: {q2:.2f}', va='center', ha='left', size=6)
            axes[i].text(1.1, q3, f'Q3: {q3:.2f}', va='center', ha='left', size=6)
            axes[i].text(1.1, min_val, f'Min: {min_val:.2f}', va='center', ha='left', size=6)
            axes[i].text(1.1, max_val, f'Max: {max_val:.2f}', va='center', ha='left', size=6)
            axes[i].text(1.1, mean_val, f'Mean: {mean_val:.2f}', va='center', ha='left', color='red', size=6)

            # Ajustar título de cada gráfico
            axes[i].set_title(col)
        else:
            axes[i].remove()
    
    # Eliminar ejes vacíos si hay menos gráficos que celdas
    for j in range(len(cols), len(axes)):
        axes[j].remove()
    
    if titulo:
        plt.suptitle(titulo)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    return fig


def estadisticas_graficoBarras(df, col_name, title_=None, colores=colores):
    """
    Genera un gráfico de barras verticales a partir del conteo de categorías en una columna de un DataFrame.
    La función calcula la frecuencia de cada categoría en la columna especificada, crea un DataFrame con la distribución,
    y luego visualiza esta distribución en un gráfico de barras.

    Parámetros:
    - data (pd.DataFrame): DataFrame que contiene los datos a analizar.
    - col_name (str): Nombre de la columna en el DataFrame cuyos valores serán contados para el gráfico.
    - title_ (str): Título del gráfico de barras.
    - colores (list, opcional): Lista de colores para las barras. Si es None, se utilizará un color predeterminado.

    Retorna:
    - fig (matplotlib.figure.Figure): La figura del gráfico de barras creada.
    """

    # Crear la figura, especificar tamaño y resolución
    fig, ax = plt.subplots(figsize=(12, 4))

    # Crear gráfico de barras verticales
    bars = df[col_name].plot(kind='bar', color=colores, legend=False, width=0.95)

    # Agregar títulos a las etiquetas de los ejes
    plt.ylabel('Frecuencia')
    plt.xlabel(col_name)
    plt.title(title_)

    # Agregar etiquetas de datos sobre las barras
    for bar in bars.patches:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # x-coordinate
            height,  # y-coordinate
            f'{height}',  # label
            ha='center',  # horizontal alignment
            va='bottom',
            fontsize=8  # vertical alignment
        )

    plt.tight_layout()

    return fig



###########################################################################
### BLOQUE 2. 
###########################################################################


def cats_y_nums(data):
    nums = data.select_dtypes(include=np.number).columns.tolist()
    cats = data.select_dtypes(include= 'object').columns.tolist()
    return cats,nums

def histog_mean_desv(data, n, dens=False):
    print('Histogramas de las variables numericas del dataset:')
    numericas = cats_y_nums(data)[1]
    data = data.loc[:, numericas]
    grilla = sns.FacetGrid(data.melt(), col='variable', col_wrap=n, sharex=False, sharey=False, height=5)
    grilla.map(sns.histplot, 'value', kde=dens)

    medias = data.mean()
    desviaciones = data.std()

    for ax, (variable, media, desviacion) in zip(grilla.axes.flat, zip(data.columns, medias, desviaciones)):
        ax.axvline(media, color='r', linestyle='--', label=f'Media: {media:.2f}')
        ax.axvline(media - desviacion, color='g', linestyle='--', label=f'Desv. Est.: {desviacion:.2f}')
        ax.axvline(media + desviacion, color='g', linestyle='--')
        ax.legend()

    plt.tight_layout()
    plt.show()

def cantidades_faltantes(data,t=None):
    print('Cantidades faltantes del dataset:')
    print(data.isnull().sum())
    print('% Faltantes del dataset:')
    print((data.isnull().sum()/data.shape[0])*100)
#     if t != None:
#         printtitulos('Mayores faltantes del dataset:')
#         print('Con threshold:',str(t))
#         perc = (data.isnull().sum()/data.shape[0])*100
#         print(perc[perc>=t])    
#         return list(perc[perc>=t].index)

def histog_categoricos(data,n,c=5,r=5):
    if type(data) == pd.core.series.Series:
        plt.figure(figsize=(c, r))
        valores, recuentos = data.value_counts().index, data.value_counts().values

        sns.barplot(x=valores, y=recuentos)
        plt.xlabel(data.name)
        plt.ylabel('Conteo')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()
        
    else:
        num_columnas = n
        num_filas = r
        plt.figure(figsize=(c*num_columnas, r*num_filas))

        for i, columna in enumerate(data.columns):
            plt.subplot(num_filas, num_columnas, i+1)
         
            valores, recuentos = data[columna].value_counts().index, data[columna].value_counts().values
            sns.barplot(x=valores, y=recuentos)
            plt.xlabel(columna)
            plt.ylabel('Conteo')
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()
        
def box_grouped(data, var_analisis, cats, showfliers=False, c=3, cs=15, rs=5):
    """
    Crea y devuelve una figura con gráficos de boxplot agrupados por categorías.

    Parámetros:
    - data (pd.DataFrame): DataFrame que contiene los datos.
    - var_analisis (str): Nombre de la columna numérica para el análisis.
    - cats (str o lista de str): Nombre de la columna categórica o una lista de columnas categóricas.
    - showfliers (bool, opcional): Mostrar o no los valores atípicos en los boxplots (por defecto False).
    - c (int, opcional): Número de columnas en la grilla de subgráficas (por defecto 3).
    - cs (int, opcional): Ancho de la figura (por defecto 15).
    - rs (int, opcional): Alto de cada fila en la figura (por defecto 5).

    Retorna:
    - fig (matplotlib.figure.Figure): La figura creada con los gráficos de boxplot.
    """
    if isinstance(cats, str):
        # Crear una sola figura
        fig, ax = plt.subplots(figsize=(cs, rs))
        
        sns.boxplot(data=data, x=cats, y=var_analisis, showfliers=showfliers, ax=ax)
        ax.set_title(f'{var_analisis} por {cats}')
        ax.set_xlabel(cats)
        ax.set_ylabel(var_analisis)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    else:
        num_variables = len(cats)
        num_cols = c  # Número de columnas en la grilla
        num_rows = (num_variables + num_cols - 1) // num_cols  # Número de filas necesarias

        fig, axes = plt.subplots(num_rows, num_cols, figsize=(cs, rs * num_rows), squeeze=False)

        for i, variable in enumerate(cats):
            row = i // num_cols
            col = i % num_cols
            sns.boxplot(data=data, x=variable, y=var_analisis, showfliers=showfliers, ax=axes[row, col])

            axes[row, col].set_title(f'{var_analisis} por {variable}')
            axes[row, col].set_xlabel(variable)
            axes[row, col].set_ylabel(var_analisis)
            axes[row, col].set_xticklabels(axes[row, col].get_xticklabels(), rotation=45)

        # Eliminar ejes vacíos si hay más subgráficas que columnas
        for j in range(i + 1, num_rows * num_cols):
            row = j // num_cols
            col = j % num_cols
            fig.delaxes(axes[row, col])

        plt.tight_layout()
    
    return fig
        
def uni_boxplot(data,var,showfliers=False,c=3,cs=15,rs=5):
    if isinstance(var, str):      
        plt.figure(figsize=(cs,rs))
        sns.boxplot(y=data[var])

        q1 = int(data[var].quantile(0.25))
        median = int(data[var].median())
        q3 = int(data[var].quantile(0.75))
        
        plt.text(0.5, q1, f'Q1: {q1:.2f}', verticalalignment='center', color='blue', fontsize=12)
        plt.text(0.5, median, f'Mediana: {median:.2f}', verticalalignment='center', color='green', fontsize=12)
        plt.text(0.5, q3, f'Q3: {q3:.2f}', verticalalignment='center', color='red', fontsize=12)
        
        plt.title(f'Boxplot {var}')
        plt.ylabel(f'{var}')

        plt.show()
                   
    else:
        num_variables = len(var)
        num_cols = c  # Define el número de columnas en la grilla
        num_rows = (num_variables + num_cols - 1) // num_cols  # Calcula el número de filas necesarias

        plt.figure(figsize=(cs, rs*num_rows))

        for i, variable in enumerate(var, 1):

            plt.subplot(num_rows, num_cols, i)
            sns.boxplot(y=data[variable], showfliers=showfliers)
            
            q1 = int(round(data[variable].quantile(0.25)))
            median = int(data[variable].median())
            q3 = int(data[variable].quantile(0.75))
            
            plt.text(0.5, q1, f'Q1: {q1}', verticalalignment='center', color='blue', fontsize=10)
            plt.text(0.5, median, f'Mediana: {median}', verticalalignment='center', color='green', fontsize=10)
            plt.text(0.5, q3, f'Q3: {q3}', verticalalignment='center', color='red', fontsize=10)

            plt.title(f'Boxplot {variable}')
            plt.ylabel(variable)

        plt.tight_layout()
        plt.show()
        
def contingencia(data,var,t=None):
    data_cross = data[['codigo_factura',var]]
    data_cross_unique = data_cross.drop_duplicates()
    cross_tab = pd.crosstab(index=data_cross_unique['codigo_factura'], columns=data_cross_unique[var])

    contingencia = cross_tab.T.dot(cross_tab)
    np.fill_diagonal(contingencia.values, 0)
    if t != None:
        return contingencia[contingencia > t].dropna(how='all').dropna(axis=1, how='all')
    #.fillna(0)
    else:
        return contingencia
    

def linea(data,x,y,desfase1,desfase2):
    suma = data.groupby(x)[y].sum()
    plt.figure(figsize=(10, 6))
    plt.plot(suma.index, suma.values, marker='o')
    cambio_mes = suma.diff()
    
    for i, value in enumerate(suma.values):
        cambio = cambio_mes.iloc[i]
        plt.text(suma.index[i], value -desfase1, str(int(value)), ha='center')
        if pd.notna(cambio):
            plt.text(suma.index[i], value -desfase2, f'Δ {int(cambio)}', ha='center', color='blue')

    plt.title(f'{x} vs {y}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.ylim(0)
    plt.grid(True) 

    plt.show()

def pareto1(data, cat, var, c=15, r=5, t=None, max_cat=None, corte=100, color_barras_corte='#598987', 
            color_barras_sin_corte='#E6EBE0', color_linea='#ED6A5A', escala=None):
    """
    Genera un diagrama de Pareto para visualizar la distribución acumulada de una variable categórica,
    con colores diferenciados para las categorías por debajo y por encima de un porcentaje acumulado de corte.
    Las etiquetas de las barras se pueden ajustar a miles o millones según el parámetro `escala`.

    Parámetros:
    - data (pd.DataFrame): DataFrame que contiene los datos a analizar.
    - cat (str): Nombre de la columna categórica para agrupar los datos.
    - var (str): Nombre de la columna numérica cuyo total se desea analizar.
    - c (int, opcional): Ancho de la figura del gráfico (por defecto 15).
    - r (int, opcional): Alto de la figura del gráfico (por defecto 5).
    - t (float, opcional): Umbral de porcentaje acumulado para filtrar las categorías (por defecto None, lo que significa que no se aplica filtro).
    - max_cat (int, opcional): Número máximo de categorías a mostrar (por defecto None, lo que significa que no se aplica límite).
    - corte (float, opcional): Porcentaje acumulado para definir el corte de color (por defecto 100, lo que significa que no se aplica corte).
    - color_barras_corte (str, opcional): Color de las barras para las categorías con porcentaje acumulado igual o menor al parámetro `corte` (por defecto '#598987').
    - color_barras_sin_corte (str, opcional): Color de las barras para las categorías con porcentaje acumulado mayor al parámetro `corte` (por defecto '#E6EBE0').
    - color_linea (str, opcional): Color de la línea del porcentaje acumulado (por defecto '#ED6A5A').
    - escala (str, opcional): Ajustar las etiquetas de las barras a 'miles' (K), 'millones' (M) o sin ajuste (None) (por defecto None).

    El gráfico mostrará las barras para los valores de `var` y una línea para el porcentaje acumulado de cada categoría.
    """

    # Agrupar por categoría y sumar la variable de interés
    suma = data.groupby(cat)[var].sum().reset_index()

    # Ordenar los resultados de mayor a menor
    suma = suma.sort_values(by=var, ascending=False)

    # Calcular el porcentaje acumulado
    suma['Porcentaje Acumulado'] = suma[var].cumsum() / suma[var].sum() * 100
    
    # Aplicar filtros basados en el threshold y el máximo de categorías
    if (t is not None) and (max_cat is not None):
        suma = suma[suma['Porcentaje Acumulado'] <= t].head(max_cat)
    elif t is not None:
        suma = suma[suma['Porcentaje Acumulado'] <= t]
    elif max_cat is not None:
        suma = suma.head(max_cat)
        
    fig, ax1 = plt.subplots(figsize=(c, r))
    
    # Colores de las barras basados en el corte
    suma['Color Barra'] = suma['Porcentaje Acumulado'].apply(lambda x: color_barras_corte if x <= corte else color_barras_sin_corte)

    # Gráfico de barras con colores diferenciados
    bars = ax1.bar(suma[cat], suma[var], color=suma['Color Barra'])
    ax1.set_xlabel(cat)
    ax1.set_ylabel(var, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Ajustar las etiquetas de las barras según el parámetro `escala`
    for bar in bars:
        yval = bar.get_height()
        if escala == 'K':
            yval_display = yval / 1000
            label = f"{yval_display:.0f}K"
        elif escala == 'M':
            yval_display = yval / 1_000_000
            label = f"{yval_display:.0f}M"
        else:
            label = int(yval)
        
        ax1.text(bar.get_x() + bar.get_width()/2, yval, label, va='bottom', ha='center', fontsize=10, color='black')

    # Gráfico de línea para el porcentaje acumulado
    ax2 = ax1.twinx()
    line = ax2.plot(suma[cat], suma['Porcentaje Acumulado'], color=color_linea, marker='o', linestyle='-')
    ax2.set_ylabel('Porcentaje Acumulado', color=color_linea)
    ax2.tick_params(axis='y', labelcolor=color_linea)
    ax2.set_ylim(0, 100)
    
    # Añadir etiquetas de valores en la línea del porcentaje acumulado
    for i in range(len(suma)):
        ax2.text(i, suma['Porcentaje Acumulado'].iloc[i], f"{int(suma['Porcentaje Acumulado'].iloc[i])}%", 
                 color=color_linea, ha="center", fontsize=10)

    # Título del gráfico
    plt.title(f'Diagrama de Pareto - {var} por {cat}')
    
    # Ajustar la rotación de las etiquetas del eje x
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right")

    plt.tight_layout()
    
    return fig
    

def outliers(data,var):
    #Rango Intercuartil
    unicos = data.drop_duplicates(subset=var).set_index('codigo_factura')
    columna = unicos[var]
    Q1 = columna.quantile(0.25)
    Q3 = columna.quantile(0.75)
    IQR = Q3 - Q1
    
    #Cota inferior y superior
    lb = Q1 - 1.5 * IQR
    ub = Q3 + 1.5 * IQR
    
    out = unicos[(columna < lb) | (columna > ub)]
    
    return out[[var]]
    

def guardar_grafico(fig, ruta):
    """
    Guarda una figura en la ruta especificada.

    Parámetros:
    - fig (matplotlib.figure.Figure): La figura de Matplotlib que se desea guardar.
    - ruta (str): Ruta completa del archivo donde se guardará la figura, incluyendo el nombre del archivo y la extensión.

    Ejemplo:
    >>> fig = plt.figure()
    >>> plt.plot([1, 2, 3], [4, 5, 6])
    >>> guardar_grafico(fig, 'mi_grafico.png')
    """
    try:
        fig.savefig(ruta, bbox_inches='tight')
        print(f'Figura guardada en {ruta}')
    except Exception as e:
        print(f'Error al guardar la figura: {e}')
        