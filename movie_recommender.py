# movie_recommender.py
import requests
import pickle

key = '6ef8d8bb1c71943c941a87efd2162966'

with open('E:\lang\MOVIE-RECOMMODATION-SYSTEM\MOVIES\Movies\model\movies.pkl', 'rb') as file:
    m = pickle.load(file)

with open("E:/lang/MOVIE-RECOMMODATION-SYSTEM/MOVIES/Movies/model/similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

titles = m['title']

def recommendMovie(movieName):
    movie_index = m[m['title'] == movieName].index
    recommended_movies = []

    if len(movie_index) > 0:
        movie_index = m[m['title'] == movieName].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:7]
        for i in movie_list:
            recommended_movies.append(m.iloc[i[0]].title)

    if recommended_movies:
        return recommended_movies[0:7]
    else:
        return []

def nowPlayingMovies():
    data = None
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={key}'

    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            data = response.json()
        else:
            data = "Something went wrong"
    except Exception as e:
        return e
    
    Names = []

    for i in range(0, 20):
        Names.append(data['results'][i]['title'])
    
    return Names

def getPoster():
    url1 = f'https://api.themoviedb.org/3/movie/now_playing?api_key={key}'
    path = []

    try:
        response = requests.get(url1)
        if response.status_code == 200:
            data = response.json()
    except Exception as e:
        return e
    
    for i in range(0, 20):
        path.append((data['results'][i]['poster_path']))
    
    posters = []

    url = 'https://image.tmdb.org/t/p/w500/'

    for i in range(0, 20):
        posters.append(url + path[i])
    
    return posters

def getLinks(movie):
    encoded_title = movie.replace(' ', '+')
    booking_link = f"https://in.bookmyshow.com/s/?q={encoded_title}"
    return booking_link


def getMovie(movieName):
    recommend_movie_key = f'https://api.themoviedb.org/3/search/movie?query={movieName}&api_key={key}'
    try:
        response = requests.get(recommend_movie_key)
        if response.status_code == 200:
            data = response.json()
        else:
            data = "Something went wrong"
    except Exception as e:
        return e
    
    return data

def getBanner(movieName):
    recommend_movie_key = f'https://api.themoviedb.org/3/search/movie?query={movieName}&api_key={key}'
    try:
        response = requests.get(recommend_movie_key)
        if response.status_code == 200:
            data = response.json()
        else:
            data = "Something went wrong"
    except Exception as e:
        return e
    
    path = data['results'][0]['poster_path']
    
    url = f'https://image.tmdb.org/t/p/w500/{path}'
    
    return url

import pandas as pd

movies = pd.read_csv("E:/lang/MOVIE-RECOMMODATION-SYSTEM/MOVIES/Movies/model/movies_dataset.csv")


# Pick me
def pickMe(user_answers):
    filtered_movies = movies.copy()

    # Filter based on mood
    filtered_movies = filtered_movies[filtered_movies['Mood'] == user_answers['mood']]
    
    age_preference = user_answers['age']
    if age_preference == '8':
        current_date = pd.to_datetime('today')
        filtered_movies['Release Date'] = pd.to_datetime(filtered_movies['Release Date'])
        filtered_movies = filtered_movies[filtered_movies['Release Date'] >= (current_date - pd.DateOffset(years=8))]
    elif age_preference == '10':
        current_date = pd.to_datetime('today')
        filtered_movies['Release Date'] = pd.to_datetime(filtered_movies['Release Date'])
        filtered_movies = filtered_movies[filtered_movies['Release Date'] >= (current_date - pd.DateOffset(years=10))]
    elif age_preference == '20':
        current_date = pd.to_datetime('today')
        filtered_movies['Release Date'] = pd.to_datetime(filtered_movies['Release Date'])
        filtered_movies = filtered_movies[filtered_movies['Release Date'] >= (current_date - pd.DateOffset(years=20))]
    elif age_preference == None:
        filtered_movies = filtered_movies

    filtered_movies = filtered_movies.sort_values(by='IMDb Score (1-10)', ascending=False)

    # Return a list of recommended movies
    recommended_movies = filtered_movies['Title'].tolist()[:10]  # Adjust as needed
    return recommended_movies

def getPickMeMovie(movieName):
    recommend_movie_key = f'https://api.themoviedb.org/3/search/movie?query={movieName}&api_key={key}'
    try:
        response = requests.get(recommend_movie_key)
        if response.status_code == 200:
            data = response.json()
        else:
            data = "Something went wrong"
    except Exception as e:
        return e
    
    return data

def getOTTPlatforms(movieName):
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={key}&query={movieName}'

    response = requests.get(search_url)
    data = response.json()

    if 'results' in data and data['results']:
        movie_id = data['results'][0]['id']
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={key}'

        response = requests.get(details_url)
        details = response.json()

        if 'results' in details and 'US' in details['results']:
            ott_providers = details['results']['US'].get('flatrate', [])
            return ott_providers

    return None