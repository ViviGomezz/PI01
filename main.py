from fastapi import FastAPI
from src.etl import process
import sklearn
import pandas as pd
import pickle

app = FastAPI()
#se carga el dataset transformado con la informacion de las peliculas
# se crea la funcion del evento que se ejecuta cuando se inicia por primera vez la API

@app.on_event("startup")
async def startup_event():
    global movies
    global model
    global movies_transform
    movies = pd.read_csv(
      'https://drive.google.com/uc?id=1o15w2plmoGJrUJhc0QbluyTnY0nSWd6j',
      sep=',')
    
    #se cargan las matrices con los datos estandarizados y con el modelo de recomendacion que creamos, los 
    #cuales podran ser consultados en el repositorio de GitHub
    
    with open('resources\Recomendation_Model.pkl', "rb") as f:
      model = pickle.load(f)
      
    with open('resources\Movies_Filtered_transf.pkl', "rb") as f:
      movies_transform = pickle.load(f)

#se crea la funcion peliculas_idioma, con su respectivo decorador, en donde se filtra el dataset por medio de la columnas
# 'original_language', y el indioma ingresado por el usuario, y se suma la cantidad de valores encontrados
# retornando la cantidad de peliculas en ese idioma
@app.get("/idioma")
async def peliculas_idioma( Idioma : str ):
    cantidad_idioma = (movies['original_language'] == Idioma).sum()
    return f"{cantidad_idioma} cantidad de películas fueron estrenadas en {Idioma}"
    
#se crea la funcion peliculas_duracion, con su respectivo decorador, en donde se filtra el dataset por medio de la columna
# 'title', y el nombre la pelicula ingresada por el usuario, luego se seleccionan los valores correspondientes
# a las columnas 'runtime' y 'release_year', retornando la duracion en minutos y año de creacion.
   
@app.get("/duracion")
async def peliculas_duracion( Pelicula: str ):
  filter = movies[movies['title'] == Pelicula]
  duracion= filter['runtime'].item()
  año= filter['release_year'].item()
  return f"{Pelicula} Duración: {duracion} Año: {año}"

#se crea la funcion franquicia, con su respectivo decorador, en donde se filtra el dataset por medio de la columna
# 'name' y el nombre de la franquicia ingresada por el usuario, se hace un conteo de la cantidad de peliculas
#que pertenecen a la franquicia, luego se realiza una sumatoria del total de revenue y un promedio
# de esa franquicia, retornando el nombre de franquicia, con la cantidad de peliculas, la ganancia total y ganancia promedio

@app.get("/franquicia")
async def franquicia( Franquicia: str ):
  franquicia = movies[movies['name']== Franquicia]
  cantidad_peliculas = franquicia.shape[0]
  total_recaudado = franquicia['revenue'].sum()
  promedio = franquicia['revenue'].mean()
  return f"La franquicia {Franquicia} posee {cantidad_peliculas} peliculas, una ganancia total de {total_recaudado} y una ganancia promedio de {promedio}"

#se crea la funcion peliculas_pais, con su respectivo decorador, en donde se filtra el dataset por medio de la columna
# 'countries' y el nombre del pais ingresada por el usuario, se hace un conteo de la cantidad de peliculas
#que se produjeron en ese pais, retornando la cantidad de peliculas y el nombre del pais

@app.get("/pais")
async def peliculas_pais( Pais: str ):
  pais= movies[movies['countries']== Pais]
  cantidad_peliculas = pais.shape[0]
  return f"Se produjeron {cantidad_peliculas} películas en el país {Pais}"

#se crea la funcion productoras_exitosas, con su respectivo decorador, en donde se filtra el dataset por medio de la columna
# 'productor' y el nombre del productor ingresada por el usuario, teniendo en cuenta que la pelicula puede tener varios productores
# se hace la consulta por medio de un .contains. Se hace una sumatoria del revenue total por productora y 
# un conteo de la cantidad de peliculas que dicha productora produjo, retornando dichos valores

@app.get("/productoras_exitosas")
async def productoras_exitosas( Productora: str ):
  productora= movies[movies['productor'].str.contains(Productora)]
  revenue_total = productora['revenue'].sum()
  cantidad_peliculas= productora.shape[0]
  return f"La productora {Productora} ha tenido un revenue de {revenue_total} y {cantidad_peliculas} peliculas"

#se crea la funcion get_director, con su respectivo decorador, en donde se filtra el dataset por medio de la columna
# 'directors' y el nombre del director ingresado por el usuario, teniendo en cuenta que la pelicula puede tener varios directores
# se hace la consulta por medio de un .contains. Se hace una sumatoria del return total por director y se retorna
#un diccionario con la informacion del return y de cada pelicula producida por el director

@app.get("/director")
async def get_director( nombre_director ): 
  director= movies[movies['directors'].str.contains(nombre_director)]
  retorno = director['return'].sum()
  exitos = director[['title', 'release_date', 'return', 'budget', 'revenue']]
  return {'retorno_director':retorno,
          'peliculas_director': exitos.to_dict(orient='records')}
  
#se crea la funcion recomendacion( titulo ), con su respectivo decorador, en donde se obtiene del dataset, el
# indice de cada pelicula por medio de la columna 'title', una vez obtenido el indice, se introduce dicho valor 
#en el modelo de vecinos cercanos que hemos creado con un nuevo dataset llamado movies_transform, en donde
# tenemos nuestros datos trasnformados, retornando las cinco peliculas recomendadas, las cuales buscara en el 
# dataset original movies. 

@app.get("/recomendar")
async def recomendacion( titulo ):
  index_ = movies[movies['title']==titulo].index.values.astype(int)[0]
  dif, ind = model.kneighbors(movies_transform[index_])
  movies_recomended = movies.loc[ind[0][1:], :]['title'].to_list()
  return movies_recomended
