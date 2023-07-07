import pandas as pd
import ast
import json
import csv
import numpy as np
import re
import datetime

def process():
    print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Init process ETL")
    movies = pd.read_csv('resources\movies_dataset_corregido.csv', sep=',')

    movies['belongs_to_collection'] = movies['belongs_to_collection'].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else None)
    movies2 = pd.json_normalize(movies["belongs_to_collection"])
    movies2= movies2.drop('id', axis= 1)
    movies = pd.concat([movies, movies2], axis=1,)

    def get_genre_names(genre_list):
        genres = ast.literal_eval(genre_list)
        return ", ".join([genre["name"] for genre in genres])

    movies["genres_name"] = movies["genres"].apply(get_genre_names)

    def get_country_names(country_list):
        countries = ast.literal_eval(country_list)
        return ", ".join([country["name"] for country in countries])


    movies["countries"] = movies["production_countries"].apply(get_country_names)

    def get_production_names(production_list):
        productions = ast.literal_eval(production_list)
        return ", ".join([productor["name"] for productor in productions])

    movies["productor"] = movies["production_companies"].apply(get_production_names)

    movies.drop(columns=['belongs_to_collection','genres', 'production_countries', 'production_companies'], inplace=True)

    df = pd.read_csv('resources\credits.csv')

    def get_director_names(director_list):
        crew = ast.literal_eval(director_list)
        list_directors=[]
        for job in crew:
            if job['job']== 'Director':
                list_directors.append(job['name'])
        return list_directors

    df["directors"] = df["crew"].apply(lambda x: get_director_names(x) if pd.notnull(x) else None)
    df['directors'] = df['directors'].astype(str)
    df['directors'] = df['directors'].str.strip("[]'")
    df["directors"] = df["directors"].apply(lambda x: re.sub(r'(?<=\w)([A-Z])', r' \1', x))


    df = df.drop(columns=['crew','cast'])

    df['id'] = df['id'].astype(int)
    movies = movies.dropna(how='all')
    movies['id']=movies['id'].astype(int)

    movies = pd.merge(movies,df, how='inner', left_on=['id'], right_on=['id'])

    movies['revenue'] = movies['revenue'].fillna(0)
    movies['budget'] = movies['budget'].fillna(0)

    movies['release_date'] = pd.to_datetime(movies['release_date'], format='%Y-%m-%d')

    movies = movies.dropna(subset=['release_date'])

    movies['release_year'] = movies['release_date'].dt.year

    movies['return'] = movies['revenue'] / movies['budget']
    movies['return'] = movies['return'].fillna(0)
    movies['return'].replace([np.inf], 0, inplace=True)

    movies = movies.drop(columns=['video','imdb_id','adult','original_title','poster_path', 'homepage'])
    print(f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')} End process ETL")
    return movies