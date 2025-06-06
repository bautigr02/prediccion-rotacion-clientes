# Predicción de Rotación de Clientes

## 1. Introducción
En este proyecto, se desarrolla un modelo predictivo para identificar clientes en riesgo de rotación (churn) para una empresa de telecomunicaciones. La rotación de clientes es un desafío crítico para las empresas, ya que retener clientes existentes es más rentable que adquirir nuevos.

## 2. Origen de Datos
Se utilizó un dataset de Kaggle que contiene información demográfica, de uso del servicio y comportamiento de pago de clientes.

## 3. Análisis Exploratorio de Datos (EDA)
Se realizó un análisis exhaustivo para comprender la distribución de las variables y su relación con la rotación de clientes.
- Se identificó un desbalance de clases en la variable objetivo 'Churn' (rotación: irse de la empresa como clientes).
- Observaciones clave:
    - Clientes con menor **Antigüedad** y **Frecuencia de Uso** mostraron mayor propensión a rotar.
    - La **Duración del Contrato** (especialmente mensual) fue un fuerte indicador de churn.
    - Los **Retrasos en Pagos** y un menor **Gasto Total** también se correlacionaron con la rotación.
    - Histogramas y Boxplots obtenidos:
![image](https://github.com/user-attachments/assets/5e3a2851-8ce7-4429-a500-884b768d212c)

## 4. Preprocesamiento de Datos
Se realizaron los siguientes pasos para preparar los datos para el modelado:
- Manejo de valores faltantes.
- Eliminación de columnas irrelevantes (ej., `CustomerID`).
- **Codificación One-Hot** para variables categóricas (`Gender`, `Subscription Type`, `Contract Length`) para convertirlas a formato numérico.
- **Escalado (StandardScaler)** de variables numéricas para normalizar su rango.
- **División del dataset** en conjuntos de entrenamiento y prueba (80/20) asegurando la misma proporción de clases (`stratify=y`).

## 5. Modelado Predictivo
Se entrenaron dos modelos de clasificación:
- **Regresión Logística:** Un modelo lineal, simple e interpretable.
- **Random Forest Classifier:** Un modelo de conjunto robusto y potente.

## 6. Evaluación de Modelos
Se evaluó el rendimiento de los modelos utilizando métricas clave para problemas de clasificación desbalanceados: Precision, Recall, F1-Score y AUC-ROC.

- **Regresión Logística:**
    - Accuracy: 0.8933
    - Precision: 0.9233
    - Recall: 0.8854
    - F1-Score: 0.9040
    - AUC-ROC: 0.9590
    - ![image](https://github.com/user-attachments/assets/9470ba14-878b-471f-8584-a3857948296f)


- **Random Forest:**
    - Accuracy: 0.9997
    - Precision: 0.9999
    - Recall: 0.9995
    - F1-Score: 0.9997
    - AUC-ROC: 1.0000
    - ![image](https://github.com/user-attachments/assets/9d277e72-07f8-476c-8d32-8f32319d82ac)

    - **Nota:** Los resultados del Random Forest fueron excepcionalmente altos, lo que podría sugerir un dataset "fácil" o una posible fuga de datos. Sin embargo, el modelo muestra una gran capacidad predictiva en los datos de prueba.


## 7. Interpretación y Conclusiones
El modelo **Random Forest** fue el de mejor rendimiento. Se analizaron las características más importantes que influyen en la rotación de clientes:

1.  **Llamadas a Soporte (`Support Calls`):** La característica más influyente, indicando que problemas de soporte son un motor clave de churn.
2.  **Gasto Total (`Total Spend`):** Clientes con menor gasto acumulado tienen mayor riesgo.
3.  **Edad (`Age`):** Sorprendentemente influyente para el modelo, lo que sugiere patrones complejos de churn por edad.
4.  **Duración Contrato_Mensual (`Contract Length_Monthly`):** Los contratos mensuales son un riesgo significativo de rotación.
5.  **Retraso en Pagos (`Payment Delay`):** Un indicador claro de problemas que pueden llevar al churn.
![image](https://github.com/user-attachments/assets/c77da0be-0e0a-46ce-b2a0-e48e0507f33f)


## 8. Recomendaciones de Negocio
Basado en los hallazgos del modelo, se proponen las siguientes estrategias para reducir la rotación de clientes:

- **Fortalecer el Soporte al Cliente:** Mejorar la resolución de problemas y la experiencia del cliente para reducir las llamadas repetitivas y la frustración. Implementar un monitoreo proactivo para clientes con muchas llamadas de soporte.
- **Fomentar el Compromiso y Gasto:** Desarrollar programas de fidelización, incentivos y ofertas para aumentar el uso del servicio y el gasto total, especialmente en las primeras etapas.
- **Ofrecer Incentivos para Contratos Largos:** Promocionar activamente los contratos anuales/bienales con descuentos o beneficios exclusivos para reducir la exposición a la rotación mensual.
- **Gestión Proactiva de Pagos:** Implementar sistemas de alerta temprana para retrasos en pagos y contactar a los clientes para ofrecer soluciones o recordatorios.
- **Análisis por Segmentos de Edad:** Investigar más a fondo si hay necesidades o sensibilidades específicas relacionadas con la edad del cliente.

## 9. Tecnologías Utilizadas
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

## 10. Notas Adicionales / Herramientas de Asistencia

Para la realización de este proyecto, se utilizó un modelo de lenguaje (LLM), como Gemini, como herramienta de asistencia en varias etapas del proceso. Esto incluyó:

* **Guía en el flujo de trabajo:** Asistencia en la estructuración de las etapas del proyecto (EDA, preprocesamiento, modelado).
* **Explicación de conceptos:** Clarificación de algoritmos de Machine Learning, métricas de evaluación y técnicas de preprocesamiento.
* **Depuración de código:** Ayuda en la identificación y resolución de errores.


El uso de esta herramienta facilitó y potencio el aprendizaje y la ejecución del proyecto.
