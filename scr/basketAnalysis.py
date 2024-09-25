from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth


# Función para calcular reglas de asociación utilizando Apriori
def calcular_reglas_apriori(datos, soporte_minimo=0.01, confianza_minima=0.1):
    itemsets_frecuentes = apriori(datos, min_support=soporte_minimo, use_colnames=True)
    reglas = association_rules(itemsets_frecuentes, metric="confidence", min_threshold=confianza_minima)
    return itemsets_frecuentes, reglas

# Función para calcular reglas de asociación utilizando FP-Growth
def calcular_reglas_fp_growth(datos, soporte_minimo=0.01, confianza_minima=0.1):
    itemsets_frecuentes = fpgrowth(datos, min_support=soporte_minimo, use_colnames=True)
    reglas = association_rules(itemsets_frecuentes, metric="confidence", min_threshold=confianza_minima)
    return itemsets_frecuentes, reglas

# Función para calibrar los parámetros y encontrar el mejor conjunto para Apriori
def calibrar_apriori(datos, parametros_grid):
    mejor_lift = 0
    mejor_configuracion = None
    mejores_reglas = None
    for parametros in parametros_grid:
        soporte_minimo = parametros['soporte_minimo']
        confianza_minima = parametros['confianza_minima']
        try:
            itemsets_frecuentes, reglas = calcular_reglas_apriori(datos, soporte_minimo, confianza_minima)
            if not reglas.empty:
                max_lift = reglas['lift'].max()
                if max_lift > mejor_lift:
                    mejor_lift = max_lift
                    mejor_configuracion = parametros
                    mejores_reglas = reglas
                    itemsets_frecuentes = itemsets_frecuentes
        except:
            continue
    return mejor_configuracion, mejores_reglas, itemsets_frecuentes

# Función para calibrar los parámetros y encontrar el mejor conjunto para FP-Growth
def calibrar_fp_growth(datos, parametros_grid):
    mejor_lift = 0
    mejor_configuracion = None
    mejores_reglas = None
    for parametros in parametros_grid:
        soporte_minimo = parametros['soporte_minimo']
        confianza_minima = parametros['confianza_minima']
        try:
            itemsets_frecuentes, reglas = calcular_reglas_fp_growth(datos, soporte_minimo, confianza_minima)
            if not reglas.empty:
                max_lift = reglas['lift'].max()
                if max_lift > mejor_lift:
                    mejor_lift = max_lift
                    mejor_configuracion = parametros
                    mejores_reglas = reglas
                    itemsets_frecuentes = itemsets_frecuentes
        except:
            continue
    return mejor_configuracion, mejores_reglas, itemsets_frecuentes






