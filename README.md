# Proyecto Individual 1 - Data Science
![logo](https://neurona-ba.com/wp-content/uploads/2021/07/HenryLogo.jpg)


## Presentación del problema - contexto
Se hace entrega de dos dataset, los cuales contienen información relevante para el desarrollo de una API que contenga un modelo de recomendación de películas, dicho modelo debe ser creado y entrenado para su utilización en vivo por medio de la web.

## Video presentacion del proyecto

[![Ver video](https://i9.ytimg.com/vi/4LWcHK5nK9g/mqdefault.jpg?sqp=CNyEtqUG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGCggVihyMA8=&rs=AOn4CLDHhubz4An-_7pORLhs_f4EcjhaCg)](https://youtu.be/4LWcHK5nK9g)

## Rol a desarrollar
El trabajo se desarrolló bajo el rol de un MLOps Engineer. Se requiere entregar un MVP (Minimum Viable Product) que cumpla con los criterios de evaluación establecidos:
- Transformaciones
- Desarrollo API
- Deployment
- Análisis exploratorio de los datos (EDA)
- Sistema de recomendación
- Video

## Diccionario de nuestros datos:

- budget	=	El presupuesto de la película, en dólares
- id	=	ID de la pelicula
- original_language	=	Idioma original en la que se grabo la pelicula
- overview	=	Pequeño resumen de la película
- popularity	=	Puntaje de popularidad de la película, asignado por TMDB (TheMoviesDataBase)
- release_date	=	Fecha de estreno de la película
- revenue	=	Recaudación de la pelicula, en dolares
- runtime	=	Duración de la película, en minutos
- spoken_languages	=	Lista con los idiomas que se hablan en la pelicula
- status	=	Estado de la pelicula actual (si fue anunciada, si ya se estreno, etc)
- tagline	=	Frase celebre asociadaa la pelicula
- title	=	Titulo de la pelicula
- vote_average	=	Puntaje promedio de reseñas de la pelicula
- vote_count	=	Numeros de votos recibidos por la pelicula, en TMDB
- name	=	Nombre de la franquicia
- backdrop_path	=	URL de la foto
- genres_name	=	Lista de generos
- countries	=	Lista de paises
- productor	=	Lista de productoras
- directors	=	Lista de directores
- release_year	=	Año de creacion
- return	=	Retorno de la pelicula, obtenido de la division de revenue y budget

## Desarrollo del Proyecto

## 1. ETL

- Algunos campos, como belongs_to_collection, production_companies y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos para poder y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

- Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

- Los valores nulos del campo release date deben eliminarse.

- De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

- Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

-  Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,poster_path y homepage


## 2. EDA

Se realiza una exploración de los datos ya transformados con el fin de entenderlos mejor y poderlos usar de la mejor forma para el desarrollo de la API. Incluyendo graficas interesantes para la extracción de los datos.
Nuestro EDA incluye:
-  Vista previa del contenido del dataset

- información general del contenido del dataset (Cantidad y tipos de datos)

- Análisis estadístico variables cuantitativas

- Análisis estadístico variables cualitativas

- Gráfico de barras de la ganancia por año, tomando los valores de revenue más significativos los cuales están entre los años 1973 y 2017

- Gráfico de dispersión entre las variables Revenue, Budget, popularity y return

- Nube de palabras



## Desarrollo API

se disponibilizan los datos usando el framework FastAPI. Las consultas que se desarrollaron son las siguientes:

- @app.get("/idioma")
def peliculas_idioma( Idioma : str ): Se ingresa un idioma, tal como están escritos en el dataset, la logica devuelve la cantidad de películas producidas en ese idioma.
                

- @app.get("/duracion")
def peliculas_duracion( Pelicula: str ): Se ingresa una pelicula. la logica devuelve la duracion y el año.
                

- @app.get("/franquicia")
def franquicia( Franquicia: str ): Se ingresa la franquicia, la logica retorna la cantidad de peliculas, ganancia total y promedio

- @app.get("/pais")
def peliculas_pais( Pais: str ): Se ingresa un país (como están escritos en el dataset), retornando la cantidad de peliculas producidas en el mismo.

- @app.get("/productoras_exitosas")
def productoras_exitosas( Productora: str ): Se ingresa la productora, retornando el revunue total y la cantidad de peliculas que realizo.


- @app.get("/director")
def get_director(nombre_director): Se ingresa el nombre de un director que se encuentre dentro de un dataset, la logica retorna  el éxito del mismo medido a través del return. Además, devuelve tambien el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.

## Deployment

Se realiza la disponibilizacion de la información por medio de Render para que de esta manera pueda ser consumida por medio de la web. Se cargan las funciones anteriormente mencionadas y el modelo de recomendación que hemos entrenado y almacenado en el archivo Recomendation_model.py, el cual nos permite cargar la matriz transformada y el modelo de recomendación al cual llamamos nneighbors.

Usamos la función @app.get("/recomendar") async def recomendacion( titulo ): Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

Dicho proceso podemos consultarlo en el archivo main.py

