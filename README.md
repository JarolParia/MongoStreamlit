# Análisis de Matrículas Escolares con MongoDB y Streamlit

## Tabla de contenido
- [1. Descripción general](#1-descripción-general)
- [2. Objetivo del proyecto](#2-objetivo-del-proyecto)
- [3. Tecnologías utilizadas](#3-tecnologías-utilizadas)
- [4. Estructura del proyecto](#4-estructura-del-proyecto)
- [5. Fuente de datos y modelo de trabajo](#5-fuente-de-datos-y-modelo-de-trabajo)
- [6. Arquitectura de la solución](#6-arquitectura-de-la-solución)
- [7. Ejecución del proyecto](#7-ejecución-del-proyecto)
- [8. Resultados generales del análisis](#8-resultados-generales-del-análisis)
- [9. Análisis detallado de los gráficos](#9-análisis-detallado-de-los-gráficos)
- [10. Hallazgos principales](#10-hallazgos-principales)
- [11. Conclusiones](#11-conclusiones)
- [12. Recomendaciones](#12-recomendaciones)

---

## 1. Descripción general

Este proyecto desarrolla una aplicación interactiva en **Streamlit** para el análisis de matrículas escolares del municipio de **San Pedro de los Milagros, Antioquia**, utilizando **MongoDB** como base de datos y un proceso **ETL** para extraer, transformar y cargar la información desde una fuente pública y desplegado mediante el uso de **Render**.

La aplicación permite:
- consultar el estado de la base de datos,
- sincronizar y actualizar la información,
- explorar registros con filtros dinámicos,
- visualizar indicadores clave de matrícula,
- identificar patrones de retiro escolar, distribución por zona, estrato, género, edad, grado y discapacidad.

---

## 2. Objetivo del proyecto

Construir un sistema de análisis de datos escolares que permita estudiar el comportamiento de la matrícula estudiantil mediante visualizaciones interactivas, apoyando la identificación de patrones relevantes para la toma de decisiones académicas y administrativas.

### Objetivos específicos
- Integrar datos de matrículas escolares desde una fuente externa.
- Almacenar y consultar la información en MongoDB.
- Desarrollar una aplicación web para exploración y análisis.
- Presentar indicadores claros sobre matrícula, retiro, edad, estrato, zona e inclusión.
- Detectar hallazgos útiles sobre distribución estudiantil y posibles factores asociados a deserción.

---

## 3. Tecnologías utilizadas

- **Python**
- **Streamlit**
- **MongoDB**
- **PyMongo**
- **Pandas**
- **Plotly**
- **Requests**
- **dotenv**

---

## 4. Estructura del proyecto

```bash
MongoStreamlit/
├── app.py
├── requirements.txt
├── dao/
│   └── mongo_dao.py
├── etl/
│   └── loader.py
├── services/
│   └── data_service.py
├── pages/
│   ├── Analisis.py
│   ├── Contexto_BD.py
│   └── Gestion_Datos.py
└── docs/
    └── images/
```

### Descripción de carpetas y archivos
- **app.py**: página principal del proyecto.
- **dao/mongo_dao.py**: capa de acceso a datos para MongoDB.
- **etl/loader.py**: proceso de extracción, limpieza y sincronización.
- **services/data_service.py**: transformaciones, agregaciones y métricas.
- **pages/Analisis.py**: visualizaciones analíticas y filtros.
- **pages/Contexto_BD.py**: exploración del esquema y registros.
- **pages/Gestion_Datos.py**: administración de sincronización y actualización.

---

## 5. Fuente de datos y modelo de trabajo

La información proviene del conjunto de datos publicado en el portal de datos abiertos de Colombia, correspondiente al sistema **SIMAT**. El proyecto trabaja con registros de **educación primaria**, enfocados en el municipio de **San Pedro de los Milagros (Antioquia)** para el año **2014**.

### Proceso general
1. **Extracción** desde la API pública.
2. **Limpieza y transformación** de campos relevantes.
3. **Cálculo de variables derivadas**, como edad y etiqueta del grado.
4. **Carga y sincronización** en MongoDB.
5. **Consulta y visualización** mediante Streamlit.

### Transformaciones relevantes del ETL
- Eliminación de campos con alta proporción de vacíos o valores no informativos.
- Conversión de `fecha_nacimiento` a formato fecha.
- Cálculo automático del campo `edad`.
- Generación de `grado_label` para mejorar la interpretación visual.
- Creación de un identificador `_id_api` para evitar duplicados.
- Sincronización inteligente mediante **upserts** y eliminación de registros obsoletos.

---

## 6. Arquitectura de la solución

### 6.1. Capa de acceso a datos
La clase `MongoDAO` centraliza la conexión a MongoDB y las operaciones principales sobre la colección. Entre sus funciones se encuentran:
- conexión y desconexión,
- creación de índices,
- inserción y actualización masiva,
- conteo de documentos,
- obtención de muestras,
- gestión de metadatos de sincronización.

### 6.2. Capa de servicio
`data_service.py` convierte los documentos en `DataFrame` de Pandas y prepara las agregaciones necesarias para los gráficos:
- conteos por campo,
- conteos por dos campos,
- distribución de edades,
- top de instituciones,
- resumen general con KPIs.

### 6.3. Capa de presentación
La aplicación está organizada en tres módulos principales:
- **Inicio**: resumen del proyecto y métricas rápidas.
- **Contexto BD**: descripción de la estructura de datos y exploración de registros.
- **Gestión de Datos**: sincronización, recarga y monitoreo de la base.
- **Análisis**: tablero interactivo con filtros y gráficos analíticos.

---

## 7. Ejecución del proyecto

### 7.1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 7.2. Configurar variables de entorno
Crear un archivo `.env` con una estructura similar a la siguiente:

```env
MONGO_URI=tu_uri_de_mongodb
DB_NAME=matriculas_antioquia
COLLECTION_NAME=estudiantes
API_URL=https://www.datos.gov.co/resource/ms9j-p68v.json
API_LIMIT=5000
```

### 7.3. Ejecutar la aplicación
```bash
streamlit run app.py
```

---

## 8. Resultados generales del análisis

<img width="1382" height="482" alt="image" src="https://github.com/user-attachments/assets/d30f8ed3-902a-48aa-af54-3051bfb709db" />

### Vista general del tablero

### Indicadores principales

| Indicador | Valor |
|---|---:|
| Total de estudiantes | **22,582** |
| Estudiantes matriculados | **21,062** |
| Estudiantes retirados | **839** |
| Estudiantes con discapacidad | **1,230** |
| Edad promedio | **10.0 años** |

### Lectura inicial de los KPIs
- La base refleja una población estudiantil amplia, con más de **22 mil registros** analizados.
- La mayor parte de los estudiantes se encuentra en estado **matriculado**, lo que evidencia una permanencia escolar alta.
- El número de **retirados** es menor frente al total, pero sigue siendo un indicador importante para detectar focos de deserción.
- La existencia de **1,230 estudiantes con discapacidad** muestra la necesidad de revisar estrategias de inclusión educativa.
- La **edad promedio de 10 años** es coherente con población de educación básica primaria, aunque los gráficos posteriores evidencian casos de extraedad y variabilidad entre grados.

---

## 9. Análisis detallado de los gráficos

### 9.1. Top instituciones por número de estudiantes

<img width="1864" height="817" alt="image" src="https://github.com/user-attachments/assets/2cca25ae-f861-4d73-917a-28e021cfcf54" />


**Interpretación:**
Este gráfico muestra las instituciones educativas que concentran la mayor cantidad de estudiantes dentro del conjunto analizado.

**Análisis:**
- La institución con mayor cantidad de estudiantes es **I.E. PIO XII**.
- Le siguen **I.E. PADRE ROBERTO ARROYAVE VÉLEZ** e **I.E.R. EL TAMBO**.
- También aparecen con participación importante **I.E. Escuela Normal Superior Señor de los Milagros**, **I.E.R. Ovejas** y **C.E.R. El Espinal**.
- La matrícula no se distribuye de manera uniforme; por el contrario, se observa una **concentración en un grupo reducido de instituciones**.

**Conclusión:**
La población estudiantil se agrupa especialmente en unas pocas instituciones, lo que puede asociarse con mayor cobertura, mejor infraestructura o centralidad geográfica. Esto sugiere la necesidad de revisar la distribución de recursos y demanda institucional.

---

### 9.2. Edad promedio por estrato y estado

<img width="712" height="542" alt="image" src="https://github.com/user-attachments/assets/2e77f5d3-496b-4ad4-b838-8c5dfc632cff" />


**Interpretación:**
Este gráfico compara la edad promedio entre estudiantes **matriculados** y **retirados** en cada estrato socioeconómico.

**Análisis:**
- En la mayoría de los estratos, los estudiantes **retirados presentan una edad promedio superior** a la de los matriculados.
- En **estrato 0**, la diferencia es muy marcada: aproximadamente **9.2 años** en matriculados frente a **12.2 años** en retirados.
- En **estrato 1**, se observa también una diferencia importante (**9.2 vs 10.3**).
- En **estrato 2** y **estrato 3**, la distancia disminuye, pero se mantiene.
- En **estrato 4**, vuelve a apreciarse una diferencia visible (**9.3 vs 10.2**).
- En categorías como **No aplica**, la brecha es menor, aunque persiste.

**Conclusión:**
La mayor edad promedio en estudiantes retirados sugiere que la **extraedad** puede estar asociada al riesgo de retiro escolar. Este patrón indica que la permanencia podría verse afectada por rezagos académicos o trayectorias escolares discontinuas.

---

### 9.3. Pirámide poblacional por edad y género

<img width="664" height="566" alt="image" src="https://github.com/user-attachments/assets/f73386d1-3574-4193-ab04-88c3b719702c" />


**Interpretación:**
La pirámide compara la distribución de estudiantes por edad y género.

**Análisis:**
- La mayor concentración de estudiantes se ubica aproximadamente entre los **7 y 11 años**.
- La distribución entre **hombres y mujeres** es relativamente equilibrada.
- En edades centrales de la primaria se observa una participación alta en ambos grupos.
- Las edades más extremas presentan menor volumen de estudiantes, como es esperable.

**Conclusión:**
La estructura por edad y género muestra una población coherente con primaria y sin desequilibrios fuertes por sexo. La matrícula presenta una base poblacional estable y homogénea entre hombres y mujeres.

---

### 9.4. Retiro vs matrícula por estrato (%)

<img width="685" height="577" alt="image" src="https://github.com/user-attachments/assets/c397e8c3-04ff-410e-945f-5d7abb7939f3" />


**Interpretación:**
El gráfico presenta la proporción de estudiantes matriculados y retirados en cada estrato.

**Análisis:**
- En todos los estratos predomina ampliamente el estado **matriculado**.
- Los porcentajes de retiro visibles son aproximadamente:
  - **Estrato 0:** 4.7%
  - **Estrato 1:** 4.8%
  - **Estrato 2:** 3.1%
  - **Estrato 3:** 2.7%
  - **Estrato 4:** 5.6%
  - **Estrato 5:** 0.0%
  - **Estrato 6:** 0.0%
  - **No aplica:** 11.3%
- La categoría **No aplica** presenta el porcentaje de retiro más alto.
- Entre los estratos convencionales, el **estrato 4** es el que evidencia mayor proporción de retiro.

**Conclusión:**
Aunque la permanencia general es alta, existen grupos donde el retiro resulta más significativo. La categoría **No aplica** y el **estrato 4** merecen una revisión más profunda para identificar causas particulares.

---

### 9.5. Dispersión de edades por grado

<img width="668" height="531" alt="image" src="https://github.com/user-attachments/assets/d1211995-2c0a-4912-87b2-cf682481cb4b" />


**Interpretación:**
Este diagrama de caja permite observar la distribución de edades por grado, incluyendo dispersión, mediana y valores atípicos.

**Análisis:**
- Se aprecia una progresión razonable de edad a medida que aumenta el grado.
- Sin embargo, existen **valores atípicos** en varios grados, especialmente estudiantes con edades superiores a las esperadas.
- La categoría **Sin clasificar / Extraedad** concentra edades altas, lo cual refuerza la presencia de trayectorias escolares no convencionales.
- También se observan casos de posible **rezago escolar** en grados bajos con edades elevadas.

**Conclusión:**
El gráfico evidencia que, aunque existe una secuencia esperada entre edad y grado, también hay casos de **extraedad** y dispersión significativa. Esto puede impactar el rendimiento académico y aumentar el riesgo de retiro.

---

### 9.6. Tasa de retiro por grado

<img width="668" height="536" alt="image" src="https://github.com/user-attachments/assets/e56fbcf0-2134-4f42-8f8b-1f200c26b8a8" />


**Interpretación:**
Este gráfico identifica los grados donde se concentra la mayor deserción escolar.

**Análisis:**
- El mayor valor se observa en **Ciclo 2**, con una tasa de retiro cercana al **32.5%**.
- La categoría **Sin clasificar / Extraedad** también presenta una tasa elevada, cercana al **17%**.
- En los grados ordinarios de primaria, la tasa de retiro es mucho menor y se mantiene alrededor de **2.8% a 4.7%**.
- **Grado 1** presenta un retiro cercano al **4.7%**, superior al de los grados 2 a 5.

**Conclusión:**
Los mayores riesgos de retiro no se concentran tanto en los grados regulares, sino en categorías especiales como **Ciclo 2** y **extraedad**, lo que sugiere una relación entre trayectorias escolares irregulares y deserción.

---

### 9.7. Proporción rural vs urbana

<img width="554" height="518" alt="image" src="https://github.com/user-attachments/assets/005e2170-1899-410a-b612-6a58fc9c09a6" />


**Interpretación:**
Este gráfico muestra la distribución de estudiantes según la zona de la sede educativa.

**Análisis:**
- La población **urbana** representa aproximadamente el **57%** del total.
- La población **rural** representa cerca del **43%**.
- La categoría **ND** tiene una proporción mínima, prácticamente irrelevante en términos globales.

**Conclusión:**
La matrícula tiene una ligera concentración urbana, aunque la participación rural sigue siendo muy significativa. Esto indica que las estrategias educativas deben contemplar tanto la cobertura urbana como rural.

---

### 9.8. Tipos de discapacidad reportada

<img width="655" height="502" alt="image" src="https://github.com/user-attachments/assets/814a1527-9714-4060-a4c2-694b58e6b3d9" />


**Interpretación:**
El gráfico resume la distribución de los tipos de discapacidad reportados dentro de la población estudiantil.

**Análisis:**
- La categoría **No aplica** concentra aproximadamente el **94.6%** de los registros.
- Entre los casos reportados, la discapacidad con mayor presencia es la **discapacidad intelectual**, con cerca de **1.98%**.
- Le siguen, con proporciones mucho menores, la **discapacidad psicosocial**, **múltiple**, **física**, **visual** y **auditiva**.
- Aunque el porcentaje total de discapacidad es relativamente bajo frente al universo general, su presencia no es marginal y requiere atención institucional.

**Conclusión:**
Los casos de discapacidad representan una porción específica de la población estudiantil y deben ser atendidos con enfoques diferenciales. La mayor participación de discapacidad intelectual señala un posible foco prioritario de apoyo pedagógico.

---

## 10. Hallazgos principales

1. **Alta permanencia escolar:** la mayoría de los registros corresponde a estudiantes matriculados.
2. **Concentración institucional:** unas pocas instituciones agrupan gran parte de la matrícula.
3. **Extraedad asociada al retiro:** los estudiantes retirados tienden a presentar mayor edad promedio.
4. **Deserción focalizada:** el retiro se concentra con mayor fuerza en **Ciclo 2** y en la categoría **Sin clasificar / Extraedad**.
5. **Distribución territorial mixta:** existe una leve mayoría urbana, pero con fuerte presencia rural.
6. **Población con discapacidad identificable:** se registran casos que requieren estrategias de inclusión y acompañamiento.
7. **Trayectorias heterogéneas:** la dispersión de edades por grado evidencia rezago y variabilidad en el recorrido escolar.

---

## 11. Conclusiones

El análisis de la base de datos de matrículas escolares permite afirmar que el sistema educativo evaluado presenta una **alta proporción de permanencia**, pero también muestra focos específicos que requieren atención.

La información sugiere que la **deserción no se distribuye de manera uniforme**: aparece con mayor intensidad en grupos con trayectorias menos estables, especialmente en categorías asociadas a **extraedad** y ciclos especiales. A su vez, la concentración de estudiantes en ciertas instituciones y la distribución territorial entre zona urbana y rural evidencian la necesidad de una planeación diferenciada.

En conjunto, el proyecto demuestra cómo una solución construida con MongoDB y Streamlit puede convertir una base de datos educativa en una herramienta útil para el análisis, la exploración y la toma de decisiones.

---

## 12. Recomendaciones

- Realizar seguimiento específico a estudiantes en condición de **extraedad**.
- Revisar las causas del alto retiro en **Ciclo 2** y en la categoría **No aplica**.
- Diseñar estrategias de acompañamiento focalizado para instituciones con mayor volumen de matrícula.
- Fortalecer mecanismos de inclusión para estudiantes con discapacidad.
- Profundizar en el análisis por sede, grado e institución para detectar patrones más detallados.
- Implementar más controles de calidad de datos para categorías poco definidas o ambiguas.

---
