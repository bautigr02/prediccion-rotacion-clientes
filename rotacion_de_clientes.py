# -*- coding: utf-8 -*-
"""Rotacion_de_Clientes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gVgTUrRcoeL3GyNzJKrTOxZhHh1qFbA2

# 1. Introduccion

En este proyecto, se desarrolla un modelo predictivo para identificar clientes en riesgo de rotación (churn) para una empresa de telecomunicaciones. La rotación de clientes es un desafío crítico para las empresas, ya que **retener clientes** existentes es más rentable que adquirir nuevos.

Para eso, importaremos un dataset obtenido en Kaggle:

- customer churn dataset:
customer_churn_dataset-training-master.csv

- Tambien podras obtener el archivo en el repositorio de Github

# 2. Análisis Exploratorio de Datos (EDA)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carga del dataset
try:
    df = pd.read_csv('customer_churn_dataset-training-master.csv')
    print("Dataset cargado exitosamente.")
except FileNotFoundError:
    print("Error: El archivo 'customer_churn_dataset-training-master.csv' no se encontró.")

df.head() #Primeros registros

df.tail() #Ultimos registros

df.shape # (Filas,Columnas)

df.info() #Info de cada atributo

df.columns #Atributos

numerical_cols=df.select_dtypes(include='number').columns #Columnas tipo 'number'
print(numerical_cols)

categorical_cols=df.select_dtypes(include='object').columns #Columnas tipo 'object'
print(categorical_cols)

df['Churn'].value_counts() #Valores posibles de la columna 'Churn'

"""En un total de 440833 registros:

- 249999 churn - Rotaron (Se fueron)

- 190833 No churn - No rotaron (se quedaron)


A continuacion, profundizaremos el analisis
"""

# Aseguramos que df esté cargado y con los NaNs eliminados

if 'CustomerID' in df.columns:
    df.drop('CustomerID', axis=1, inplace=True)
    print("Columna 'CustomerID' eliminada del DataFrame.")
else:
    print("La columna 'CustomerID' no se encontró o ya fue eliminada.")

# Actualizamos lista de columnas numéricas después de eliminar 'CustomerID'
numerical_cols=df.select_dtypes(include='number').columns #Columnas del tipo
print("Columnas numéricas actualizadas:", numerical_cols)

# Definimos el número de filas y columnas para la cuadrícula de gráficos
num_cols_num = len(numerical_cols)
num_rows_num = num_cols_num # Una fila por cada variable numérica, con 2 gráficos cada una

plt.figure(figsize=(16, num_rows_num * 6)) # Ajustamos el tamaño de la figura
plt.suptitle('Análisis de Churn por Variables Numéricas', fontsize=20, y=1.02)

for i, col in enumerate(numerical_cols):
    # Histograma con KDE para ver la distribución
    plt.subplot(num_rows_num, 2, 2 * i + 1)
    sns.histplot(data=df, x=col, hue='Churn', kde=True, palette='viridis', common_norm=False)
    plt.title(f'Distribución de {col} por Churn (Histograma)')
    plt.xlabel(col)
    plt.ylabel('Conteo de Clientes')

    # Boxplot para ver medianas, cuartiles y outliers
    plt.subplot(num_rows_num, 2, 2 * i + 2)
    sns.boxplot(data=df, y=col, x='Churn', palette='viridis')
    plt.title(f'Distribución de {col} por Churn (Boxplot)')
    plt.xlabel('Churn (0: No Churn, 1: Churn)')
    plt.ylabel(col)

plt.tight_layout(rect=[0, 0.03, 1, 0.98])
plt.show()

"""## Conclusiones EDA

Los que **rotan** (churn) tienden a tener **menos antigüedad** (es decir, llevan menos tiempo siendo clientes).
El boxplot muestra claramente que a mayor antigüedad, menor probabilidad de rotar.


---


Los que se quedan(no churn) tienden a usar el servicio con mayor frecuencia.
**Mayor uso** significa que **se quedan.**


---


Los que hacen **más llamadas a soporte**, más probabilidad de **Rotar** (churn).


---


**Mayor Payment Delay** asociado con **más Churn**.
Los que se quedan suelen pagar más puntualmente.


---


Los clientes que **se quedan gastan más**.
No churn asociado a mas gastos.


---


Los que **se quedan** (no churn) suelen **interactuar más recientemente**.
Los que hacen Churn tienen un mayor número de días desde su última interacción.

# 3. Preprocesamiento

## Codificar variables categoricas
"""

import pandas as pd
import numpy as np

# Primero, identificamos las columnas categóricas en el DataFrame.
categorical_cols = df.select_dtypes(include='object').columns.tolist()

# Aseguramos que Churn sea numerica
if 'Churn' in categorical_cols:
    categorical_cols.remove('Churn')

print("Columnas categóricas identificadas para codificación:", categorical_cols)

# Aplicamos One-Hot Encoding
# Creamos un nuevo DataFrame 'df_encoded' para almacenar el resultado
# La función pd.get_dummies() es la que realiza el One-Hot Encoding
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

print("\n--- Resultados después de One-Hot Encoding ---")
print("Dimensiones del DataFrame después de One-Hot Encoding (filas, columnas):", df_encoded.shape)
print("\nPrimeras 5 filas del DataFrame con columnas categóricas codificadas:")
print(df_encoded.head())

# Verificamos que las columnas categóricas originales fueron reemplazadas
print("\nVerificando que las columnas categóricas originales ya no están (deben dar KeyError si intentamos acceder):")
for col in categorical_cols:
    if col in df_encoded.columns:
        print(f"ERROR: La columna '{col}' original todavía está en el DataFrame codificado.")
    else:
        print(f"OK: La columna '{col}' original fue reemplazada.")

# Confirmamos el efecto del One-Hot Encoding
print("\nNombres de algunas de las nuevas columnas binarias creadas:")
# Filtra las columnas que terminan con '_True', '_False', '_Male', etc. o contienen un '_'
newly_encoded_cols_sample = [col for col in df_encoded.columns if any(cat_col in col for cat_col in categorical_cols) and '_' in col]
print(newly_encoded_cols_sample[:10]) # Muestra solo las primeras

"""## Escalado de Variables Numéricas"""

from sklearn.preprocessing import StandardScaler

# Identificamos las columnas numéricas en el DataFrame df_encoded.
# 'Churn' es la variable objetivo y NO se escala.
# Las columnas binarias creadas por One-Hot Encoding (True/False o 0/1) tampoco necesitan escalado.
numeric_cols_to_scale = df_encoded.select_dtypes(include=['int64', 'float64']).columns.tolist()

# Aseguramos de que 'Churn' no esté en la lista de columnas a escalar
if 'Churn' in numeric_cols_to_scale:
    numeric_cols_to_scale.remove('Churn')

print("\nColumnas numéricas identificadas para escalar:", numeric_cols_to_scale)

# Inicializar el StandardScaler
scaler = StandardScaler()

# Ajustamos el escalador a los datos numéricos y luego transformarlos.
df_scaled = df_encoded.copy()
df_scaled[numeric_cols_to_scale] = scaler.fit_transform(df_scaled[numeric_cols_to_scale])

print("\n--- Resultados después del Escalado de Variables Numéricas ---")
print("\nPrimeras 5 filas del DataFrame con columnas numéricas escaladas:")
print(df_scaled.head())

# Verificar las estadísticas descriptivas de las columnas escaladas
print("\nEstadísticas descriptivas de columnas numéricas después del escalado:")
print(df_scaled[numeric_cols_to_scale].describe())
# Deberíamos ver que la 'mean' de estas columnas es muy cercana a 0 y 'std' (desviación estándar) es muy cercana a 1.

"""# 4. Modelo predictivo

## Division del dataset
"""

from sklearn.model_selection import train_test_split

# df_scaled - DataFrame completamente preprocesado
# Identificamos características (X) y tu variable objetivo (y)

# X contendrá todas las columnas excepto 'Churn'
X = df_scaled.drop('Churn', axis=1)

# y contendrá solo la columna 'Churn'
y = df_scaled['Churn']

print("Dimensiones de X (características):", X.shape)
print("Dimensiones de y (variable objetivo):", y.shape)

# Dividimos los datos en conjuntos de entrenamiento y prueba
# test_size=0.20 significa que el 20% de los datos se usarán para la prueba, 80% para el entrenamiento
# random_state=42 asegura que la división sea reproducible (siempre obtendrás los mismos conjuntos)
# stratify=y es CRUCIAL para problemas con desbalance de clases (como el tuyo).
# Asegura que la proporción de clases (Churn vs No Churn) sea la misma en los conjuntos de entrenamiento y prueba.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

print("\nDimensiones de X_train (características de entrenamiento):", X_train.shape)
print("Dimensiones de X_test (características de prueba):", X_test.shape)
print("Dimensiones de y_train (objetivo de entrenamiento):", y_train.shape)
print("Dimensiones de y_test (objetivo de prueba):", y_test.shape)

# Verificamos la proporción de clases en y_train y y_test (deberían ser similares)
print("\nProporción de clases en y_train:")
print(y_train.value_counts(normalize=True))
print("\nProporción de clases en y_test:")
print(y_test.value_counts(normalize=True))

"""## Seleccion y entrenamiento de modelos"""

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Regresión Logística ---
print("--- Entrenando Modelo de Regresión Logística ---")
log_reg_model = LogisticRegression(random_state=42, solver='liblinear') # 'liblinear' es un buen solver para datasets pequeños/medianos
log_reg_model.fit(X_train, y_train)

# Predicciones
y_pred_log_reg = log_reg_model.predict(X_test)
y_proba_log_reg = log_reg_model.predict_proba(X_test)[:, 1] # Probabilidades para la clase positiva (Churn=1)

# --- 2. Random Forest Classifier ---
print("\n--- Entrenando Modelo Random Forest ---")
# n_estimators: número de árboles en el bosque
# class_weight='balanced' es útil para datasets desbalanceados, ajusta el peso de las clases automáticamente
rand_forest_model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rand_forest_model.fit(X_train, y_train)

# Predicciones
y_pred_rand_forest = rand_forest_model.predict(X_test)
y_proba_rand_forest = rand_forest_model.predict_proba(X_test)[:, 1] # Probabilidades para la clase positiva (Churn=1)

print("\nModelos entrenados. Listos para la evaluación.")

"""##  Evaluación del Modelo"""

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model_name, y_true, y_pred, y_proba):
    """
    Función para evaluar un modelo de clasificación y mostrar métricas.
    """
    print(f"\n--- Evaluación del Modelo: {model_name} ---")

    # Matriz de Confusión
    cm = confusion_matrix(y_true, y_pred)
    print("Matriz de Confusión:")
    print(cm)

    # Visualizar la matriz de confusión (muy útil)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['No Churn (0)', 'Churn (1)'])
    disp.plot(cmap=plt.cm.Blues)
    plt.title(f'Matriz de Confusión: {model_name}')
    plt.show()

    # Métricas de Clasificación
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_proba) # Para AUC-ROC, necesitamos las probabilidades

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"AUC-ROC:   {roc_auc:.4f}")

# Evalua Regresión Logística
evaluate_model('Regresión Logística', y_test, y_pred_log_reg, y_proba_log_reg)

# Evalua Random Forest
evaluate_model('Random Forest', y_test, y_pred_rand_forest, y_proba_rand_forest)

"""## Interpretacion del modelo"""

# Asegurarse de que rand_forest_model ya ha sido entrenado.

print("\n--- Importancia de las Características (Feature Importance) del Modelo Random Forest ---")

# Obtenemos la importancia de las características
feature_importances = rand_forest_model.feature_importances_

# Creamos DataFrame para visualizar la importancia de cada característica
features_df = pd.DataFrame({
    'Feature': X_train.columns, # Los nombres de tus columnas de características
    'Importance': feature_importances
})

# Ordena por importancia de forma descendente
features_df = features_df.sort_values(by='Importance', ascending=False)

# Muestra las características más importantes
print(features_df)

plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=features_df)
plt.title('Importancia de las Características en el Modelo Random Forest')
plt.xlabel('Importancia (Gini Importance)')
plt.ylabel('Característica')
plt.show()

"""# 5. Conclusiones y recomendaciones

### Mejora de la Experiencia con el Soporte al Cliente:
Insight: Support Calls es la característica más crítica. Un alto número de llamadas a soporte es la señal de alerta más fuerte para la rotación.
Recomendación: Implementar un sistema de monitoreo proactivo de las interacciones de soporte. Identificar y priorizar a los clientes con múltiples llamadas, baja resolución en el primer contacto o llamadas de alta frustración. Mejorar la capacitación del personal de soporte y la calidad de la resolución de problemas para reducir la necesidad de llamadas recurrentes.


---


### Estrategias para Aumentar el Gasto y el Compromiso del Cliente:
Insight: Total Spend es la segunda característica más importante. Clientes con un gasto total bajo tienen más probabilidades de rotar.
Recomendación: Desarrollar programas de fidelización, incentivos y ofertas personalizadas para aumentar el uso del servicio y el gasto del cliente. Fomentar el "upselling" o "cross-selling" de productos/servicios adicionales para aumentar su valor percibido.


---


### Análisis por Segmentos de Edad y Campañas Personalizadas:
Insight: La Age es una característica importante en el modelo.
Recomendación: Aunque el EDA inicial no mostró una correlación simple, el modelo encontró patrones complejos. Esto sugiere la necesidad de investigar si ciertos rangos de edad tienen necesidades o puntos de dolor específicos. Desarrollar campañas de retención o marketing dirigidas a segmentos de edad específicos podría ser efectivo.


---


### Incentivos para Contratos a Largo Plazo:
Insight: Los clientes con Contract Length_Monthly son un grupo de alto riesgo.
Recomendación: Ofrecer descuentos sustanciales, beneficios premium o características exclusivas para incentivar la migración de contratos mensuales a anuales o bienales. Destacar el valor a largo plazo de los contratos más extensos.


---


### Gestión Proactiva de Retrasos en Pagos:
Insight: Los Payment Delay son un predictor fuerte de churn.
Recomendación: Establecer alertas tempranas para retrasos en pagos. Contactar proactivamente a estos clientes para entender la situación, ofrecer planes de pago flexibles o recordatorios amigables. Esto puede prevenir la rotación antes de que sea inevitable.
"""