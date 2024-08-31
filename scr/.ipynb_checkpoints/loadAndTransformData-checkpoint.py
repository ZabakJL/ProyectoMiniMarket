import pandas as pd
import os

def cargar_csv(ruta):
    """
    Carga un archivo CSV en un DataFrame de pandas.

    Parámetros:
    ruta (str): La ruta completa del archivo CSV.

    Retorna:
    pd.DataFrame: Un DataFrame con los datos del archivo CSV.
    """
    try:
        df = pd.read_csv(ruta)
        print("Archivo cargado correctamente.")
        return df
    except FileNotFoundError:
        print(f"El archivo en la ruta '{ruta}' no fue encontrado.")
    except pd.errors.EmptyDataError:
        print("El archivo está vacío.")
    except pd.errors.ParserError:
        print("Error al parsear el archivo. Asegúrate de que sea un archivo CSV válido.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

# Ejemplo de uso
# df = cargar_csv("ruta/al/archivo.csv")



def dividir_y_guardar_csv(df, col_fecha, tipo_fraccionamiento, ruta_destino, nombre_archivo):
    """
    Divide un DataFrame por la columna de fecha según el año, mes o día, 
    y guarda los archivos CSV resultantes en la ruta especificada.

    Parámetros:
    df (pd.DataFrame): El DataFrame a dividir.
    col_fecha (str): El nombre de la columna que contiene las fechas.
    tipo_fraccionamiento (str): El tipo de fraccionamiento ('año', 'mes', 'dia').
    ruta_destino (str): La ruta donde se guardarán los archivos CSV.
    nombre_archivo (str): El nombre base de los archivos CSV.
    """
    # Asegurarse de que la columna de fecha esté en formato datetime
    df[col_fecha] = pd.to_datetime(df[col_fecha])
    
    # Crear la ruta de destino si no existe
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)
    
    if tipo_fraccionamiento == 'año':
        fraccionado = df.groupby(df[col_fecha].dt.year)
        sufijo = '%Y'
    elif tipo_fraccionamiento == 'mes':
        fraccionado = df.groupby([df[col_fecha].dt.year, df[col_fecha].dt.month])
        sufijo = '%Y_%m'
    elif tipo_fraccionamiento == 'dia':
        fraccionado = df.groupby([df[col_fecha].dt.year, df[col_fecha].dt.month, df[col_fecha].dt.day])
        sufijo = '%Y_%m_%d'
    else:
        print("Tipo de fraccionamiento no válido. Debe ser 'año', 'mes' o 'dia'.")
        return
    
    for grupo, datos in fraccionado:
        if tipo_fraccionamiento == 'año':
            archivo_sufijo = f"{grupo}"
        elif tipo_fraccionamiento == 'mes':
            archivo_sufijo = f"{grupo[0]}_{str(grupo[1]).zfill(2)}"
        elif tipo_fraccionamiento == 'dia':
            archivo_sufijo = f"{grupo[0]}_{str(grupo[1]).zfill(2)}_{str(grupo[2]).zfill(2)}"
        
        archivo_completo = f"{nombre_archivo}_{archivo_sufijo}.csv"
        ruta_completa = os.path.join(ruta_destino, archivo_completo)
        
        datos.to_csv(ruta_completa, index=False)
        print(f"Archivo guardado: {ruta_completa}")

# Ejemplo de uso
# dividir_y_guardar_csv(df, 'fecha', 'mes', 'ruta/a/guardar', 'nombre_archivo')
