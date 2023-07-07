from fastapi import FastAPI
from src.etl import process
import pandas as pd

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global movies
    movies = process()
    
@app.get("/idioma")
async def peliculas_idioma( Idioma : str ):
    cantidad_idioma = (movies['original_language'] == Idioma).shape[0]
    return f"{cantidad_idioma} cantidad de películas fueron estrenadas en {Idioma}"
    
@app.get("/duracion")
async def peliculas_duracion( Pelicula: str ):
  filter = movies[movies['title'] == Pelicula]
  duracion= filter['runtime'].item()
  año= filter['release_year'].item()
  return f"{Pelicula} Duración: {duracion} Año: {año}"

@app.get("/franquicia")
async def franquicia( Franquicia: str ):
  franquicia = movies[movies['name']== Franquicia]
  cantidad_peliculas = franquicia.shape[0]
  total_recaudado = franquicia['revenue'].sum()
  promedio = franquicia['revenue'].mean()
  return f"La franquicia {Franquicia} posee {cantidad_peliculas} peliculas, una ganancia total de {total_recaudado} y una ganancia promedio de {promedio}"

@app.get("/pais")
async def peliculas_pais( Pais: str ):
  pais= movies[movies['countries']== Pais]
  cantidad_peliculas = pais.shape[0]
  return f"Se produjeron {cantidad_peliculas} películas en el país {Pais}"

@app.get("/productoras_exitosas")
async def productoras_exitosas( Productora: str ):
  productora= movies[movies['productor'].str.contains(Productora)]
  revenue_total = productora['revenue'].sum()
  cantidad_peliculas= productora.shape[0]
  return f"La productora {Productora} ha tenido un revenue de {revenue_total} y {cantidad_peliculas} peliculas"

@app.get("/director")
def get_director( nombre_director ): 
  director= movies[movies['directors'].str.contains(nombre_director)]
  retorno = director['return'].sum()
  exitos = director[['title', 'release_date', 'return', 'budget', 'revenue']]
  return {'retorno_director':retorno,
          'peliculas_director': exitos.to_dict(orient='records')}

