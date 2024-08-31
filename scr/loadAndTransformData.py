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

def combinar_csv_por_prefijo(directorio, prefijo):
    """
    Combina todos los archivos CSV en un directorio cuyo nombre comience con un prefijo dado en un solo DataFrame.

    Parámetros:
    directorio (str): El directorio donde se encuentran los archivos CSV.
    prefijo (str): El prefijo que deben tener los archivos CSV a combinar.

    Retorna:
    pd.DataFrame: Un DataFrame combinado de todos los archivos CSV que cumplen con el criterio.
    """
    archivos_csv = [f for f in os.listdir(directorio) if f.startswith(prefijo) and f.endswith('.csv')]
    
    if not archivos_csv:
        print(f"No se encontraron archivos que comiencen con '{prefijo}' en el directorio '{directorio}'.")
        return pd.DataFrame()  # Devuelve un DataFrame vacío si no se encuentran archivos
    
    lista_df = []
    
    for archivo in archivos_csv:
        ruta_completa = os.path.join(directorio, archivo)
        try:
            df = pd.read_csv(ruta_completa)
            lista_df.append(df)
        except Exception as e:
            print(f"No se pudo leer el archivo '{archivo}'. Error: {e}")
    
    if lista_df:
        df_combinado = pd.concat(lista_df, ignore_index=True)
        return df_combinado
    else:
        print("No se pudo combinar ningún archivo. Verifica que los archivos estén correctamente formateados.")
        return pd.DataFrame()
    
def pivotear_df(df, columnas_unica, columna_valores):
    """
    Crea un DataFrame pivoteado donde las filas son los valores únicos de la columna 
    especificada por 'columnas_unicas', y las columnas son los valores de 'columna_valores'.

    Parámetros:
    df (pd.DataFrame): El DataFrame original.
    columnas_unicas (str): Nombre de la columna cuyas combinaciones no deben repetirse.
    columna_valores (str): Nombre de la columna cuyos valores se convertirán en nuevas columnas.

    Retorna:
    pd.DataFrame: Un DataFrame pivoteado con 1 y 0 como valores.
    """
    # Verificar que los argumentos son cadenas
    if not isinstance(columnas_unica, str):
        raise ValueError("El argumento 'columnas_unicas' debe ser una cadena.")
    if not isinstance(columna_valores, str):
        raise ValueError("El argumento 'columna_valores' debe ser una cadena.")
    
    # Crear una tabla cruzada con la columna única como índice y los valores como columnas
    df_pivot = pd.crosstab(df[columnas_unica], df[columna_valores])
    

    return df_pivot

def guardar_csv(df, ruta, nombre_archivo):
    """
    Guarda un DataFrame en un archivo CSV.

    Parámetros:
    df (pd.DataFrame): El DataFrame que se desea guardar.
    ruta (str): La ruta del directorio donde se guardará el archivo.
    nombre_archivo (str): El nombre del archivo CSV a crear (sin extensión).

    Ejemplo:
    guardar_csv(df, '/ruta/al/directorio', 'nombre_archivo')
    """
    # Asegurarse de que la ruta tenga una barra al final
    if not ruta.endswith('/'):
        ruta += '/'
    
    # Crear la ruta completa del archivo
    ruta_completa = ruta + nombre_archivo + '.csv'
    
    try:
        # Guardar el DataFrame en formato CSV
        df.to_csv(ruta_completa, index=False)
        print(f"Archivo guardado exitosamente en: {ruta_completa}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")