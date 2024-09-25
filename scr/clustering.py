import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
import matplotlib.pyplot as plt
from sklearn.model_selection import ParameterGrid
import loadAndTransformData as ltd

# Cargar los datos
ruta_archivo = '../data/processed/Minimarket_Sales_Data_Transform_By_Subcategory.csv'
datos = ltd.cargar_csv(ruta_archivo)
datos = ltd.convertir_a_bool(datos)



# Función para calcular reglas de asociación utilizando Apriori
def calcular_reglas_apriori(datos, soporte_minimo=0.01, confianza_minima=0.1):
    itemsets_frecuentes = apriori(datos, min_support=soporte_minimo, use_colnames=True)
    reglas = association_rules(itemsets_frecuentes, metric="confidence", min_threshold=confianza_minima)
    return reglas

# Función para calcular reglas de asociación utilizando FP-Growth
def calcular_reglas_fp_growth(datos, soporte_minimo=0.01, confianza_minima=0.1):
    itemsets_frecuentes = fpgrowth(datos, min_support=soporte_minimo, use_colnames=True)
    reglas = association_rules(itemsets_frecuentes, metric="confidence", min_threshold=confianza_minima)
    return reglas

# Función para calibrar los parámetros y encontrar el mejor conjunto para Apriori
def calibrar_apriori(datos, parametros_grid):
    mejor_lift = 0
    mejor_configuracion = None
    mejores_reglas = None
    for parametros in parametros_grid:
        soporte_minimo = parametros['soporte_minimo']
        confianza_minima = parametros['confianza_minima']
        try:
            reglas = calcular_reglas_apriori(datos, soporte_minimo, confianza_minima)
            if not reglas.empty:
                max_lift = reglas['lift'].max()
                if max_lift > mejor_lift:
                    mejor_lift = max_lift
                    mejor_configuracion = parametros
                    mejores_reglas = reglas
        except:
            continue
    return mejor_configuracion, mejores_reglas

# Función para calibrar los parámetros y encontrar el mejor conjunto para FP-Growth
def calibrar_fp_growth(datos, parametros_grid):
    mejor_lift = 0
    mejor_configuracion = None
    mejores_reglas = None
    for parametros in parametros_grid:
        soporte_minimo = parametros['soporte_minimo']
        confianza_minima = parametros['confianza_minima']
        try:
            reglas = calcular_reglas_fp_growth(datos, soporte_minimo, confianza_minima)
            if not reglas.empty:
                max_lift = reglas['lift'].max()
                if max_lift > mejor_lift:
                    mejor_lift = max_lift
                    mejor_configuracion = parametros
                    mejores_reglas = reglas
        except:
            continue
    return mejor_configuracion, mejores_reglas

# Crear un grid de parámetros para probar
parametros_grid = list(ParameterGrid({
    'soporte_minimo': [0.01, 0.02, 0.03],
    'confianza_minima': [0.1, 0.2, 0.3]
}))


# Calibrar Apriori
mejor_configuracion_apriori, mejores_reglas_apriori = calibrar_apriori(datos, parametros_grid)

# Calibrar FP-Growth
mejor_configuracion_fp, mejores_reglas_fp = calibrar_fp_growth(datos, parametros_grid)

# Mostrar la mejor configuración para Apriori
print("Mejor configuración Apriori:", mejor_configuracion_apriori)
# Mostrar el top 10 de reglas de Apriori
print(mejores_reglas_apriori.sort_values(by='lift', ascending=False).head(20))

# Mostrar la mejor configuración para FP-Growth
print("Mejor configuración FP-Growth:", mejor_configuracion_fp)
# Mostrar el top 10 de reglas de FP-Growth
print(mejores_reglas_fp.sort_values(by='lift', ascending=False).head(20))

# Función para calcular reglas de asociación utilizando Apriori
def calcular_reglas_apriori(datos, soporte_minimo=0.01, confianza_minima=0.1):
    # Aplicar el algoritmo apriori para encontrar itemsets frecuentes
    itemsets_frecuentes = apriori(datos, min_support=soporte_minimo, use_colnames=True)
    # Calcular las reglas de asociación basadas en estos itemsets
    reglas = association_rules(itemsets_frecuentes, metric="confidence", min_threshold=confianza_minima)
    return reglas

# Función para calcular reglas de asociación utilizando FP-Growth
def calcular_reglas_fp_growth(datos, soporte_minimo=0.01, confianza_minima=0.1):
    # Aplicar el algoritmo FP-Growth para encontrar itemsets frecuentes
    itemsets_frecuentes = fpgrowth(datos, min_support=soporte_minimo, use_colnames=True)
    # Calcular las reglas de asociación basadas en estos itemsets
    reglas = association_rules(itemsets_frecuentes, metric="confidence", min_threshold=confianza_minima)
    return reglas

# Calibrar los parámetros para Apriori
soporte_minimo_apriori = 0.02  # Ajustar según el análisis
confianza_minima_apriori = 0.3  # Ajustar según el análisis

# Calibrar los parámetros para FP-Growth
soporte_minimo_fp = 0.02  # Ajustar según el análisis
confianza_minima_fp = 0.3  # Ajustar según el análisis

# Calcular reglas utilizando Apriori
reglas_apriori = calcular_reglas_apriori(datos, soporte_minimo=soporte_minimo_apriori, confianza_minima=confianza_minima_apriori)

# Calcular reglas utilizando FP-Growth
reglas_fp_growth = calcular_reglas_fp_growth(datos, soporte_minimo=soporte_minimo_fp, confianza_minima=confianza_minima_fp)

# Mostrar las reglas más relevantes de Apriori
reglas_apriori_ordenadas = reglas_apriori.sort_values(by='lift', ascending=False).head(10)
print("Reglas de Asociación (Apriori) - Top 10")
print(reglas_apriori_ordenadas)

# Mostrar las reglas más relevantes de FP-Growth
reglas_fp_growth_ordenadas = reglas_fp_growth.sort_values(by='lift', ascending=False).head(10)
print("\nReglas de Asociación (FP-Growth) - Top 10")
print(reglas_fp_growth_ordenadas)

# Función para graficar las reglas
def graficar_reglas(reglas, metodo):
    plt.figure(figsize=(10, 6))
    plt.scatter(reglas['support'], reglas['confidence'], c=reglas['lift'], cmap='viridis', alpha=0.7, edgecolors='k')
    plt.title(f'Reglas de Asociación - {metodo}')
    plt.xlabel('Soporte')
    plt.ylabel('Confianza')
    plt.colorbar(label='Lift')
    plt.grid(True)
    plt.show()

# Graficar reglas Apriori
graficar_reglas(reglas_apriori_ordenadas, 'Apriori')

# Graficar reglas FP-Growth
graficar_reglas(reglas_fp_growth_ordenadas, 'FP-Growth')


