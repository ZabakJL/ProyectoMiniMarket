# Descubriendo los Secretos del Carrito de Compras: Un Análisis de Canasta en un Minimarket

En el competitivo mundo del retail, conocer los hábitos de compra de los clientes es fundamental para diseñar estrategias que maximicen las ventas. Nuestro minimarket, situado en un vecindario vibrante, ha visto un crecimiento constante, pero sospechamos que hay potencial no explotado en nuestras ventas. Para capitalizar estas oportunidades, hemos decidido llevar a cabo un análisis profundo de las transacciones mediante técnicas de aprendizaje no supervisado, enfocándonos en el análisis de canasta.

## Pregunta/Problema a Resolver: 
El principal objetivo de nuestro proyecto es responder a las siguientes preguntas clave:

1.	¿Cuáles son las combinaciones de productos que los clientes suelen comprar juntos?
2.	¿Existen productos que, al ser promovidos juntos, podrían aumentar el valor de las compras?
3.	¿Podemos reorganizar la disposición de productos en el minimarket para incentivar la compra conjunta de ciertos artículos?

Para abordar estas preguntas, nos centraremos en tareas de clustering y asociación. El análisis de canasta se enfocará en descubrir reglas de asociación entre productos, mientras que el clustering podría ayudar a identificar segmentos de clientes con comportamientos de compra similares. Si encontramos que los datos son demasiado complejos o numerosos, también podríamos considerar técnicas de reducción de dimensión para simplificar la interpretación.

## Contenidos

- [**data/**](data/): Datos utilizados en el proyecto.
  - `raw/`: Datos en formato original.
  - `processed/`: Datos procesados y listos para el análisis.
  
- [**notebooks/**](notebooks/): Jupyter Notebooks que documentan el flujo de trabajo.
  - `01_data_exploration.ipynb`: Exploración inicial de los datos.
  - `02_data_transform.ipynb`: Limpieza y preprocesamiento de datos.
  - `03_basket_analysis.ipynb`: Aplicación de algoritmos de clustering.
  - `04_results_visualization.ipynb`: Visualización de resultados.
  
- [**src/**](src/): Código fuente del proyecto.
  - `loadAndTransformData.py`: Scripts para la limpieza y preprocesamiento de datos.
  - `clustering.py`: Scripts para el clustering.
  - `viedDataFunctions.py`: Scripts para la visualización de datos.

- [**reports/**](reports/): Documentación y reportes del proyecto.
  - `figures/`: Imágenes y gráficos generados.
  - `Propuesta inicial.pdf`: resumen de la propuesta de desarrollo del proyecto.

- [**weekly_updates/**](weekly_updates/): Instrucciones y avances semanales del proyecto.

