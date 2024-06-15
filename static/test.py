key = '6ef8d8bb1c71943c941a87efd2162966'
import requests

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

def getOTT(movieName):
    recommend_movie_key = f'"https://api.themoviedb.org/3/watch/providers/movie?query={movieName}&api_key={key}'
    try:
        response = requests.get(recommend_movie_key)
        if response.status_code == 200:
            data = response.json()
        else:
            data = "Something went wrong"
    except Exception as e:
        return e
    
    return data

ans = getMovie("Barbie")

# print(ans)


print(ans['results'][0]['title'])
print(ans['results'][0]['overview'])
print(ans['results'][0]['poster_path'])
print(ans['results'][0]['release_date'])
print(ans['results'][0]['vote_average'])
print(ans['results'][0]['id'])


id = ans['results'][0]['id']

import requests

url = f"https://api.themoviedb.org/3/movie/{id}/watch/providers"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZWY4ZDhiYjFjNzE5NDNjOTQxYTg3ZWZkMjE2Mjk2NiIsInN1YiI6IjY0ZjM2OGE0OWU0NTg2MDEzYWY4YjU4MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Au-vwNgVu5IJrDDD6Y-LkfxS1zh1NVKEdvXKaK9XpyU"
}

response = requests.get(url, headers=headers)

data = response.json()
# print(data['results']['AD']['flatrate'][0]['provider_name'])
# print(data)


import requests

def find_ott_platforms(movie_title):
    api_key = 'YOUR_TMDB_API_KEY'  # You need to sign up for a TMDb API key
    search_url = f'https://api.themoviedb.org/3/search/movie?api_key={key}&query={movie_title}'

    response = requests.get(search_url)
    data = response.json()

    if 'results' in data and data['results']:
        movie_id = data['results'][0]['id']
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={key}'

        response = requests.get(details_url)
        details = response.json()

        if 'results' in details and 'IN' in details['results']:
            ott_providers = details['results']['US'].get('flatrate', [])
            return ott_providers[0:1]

    return None

movie_title = 'Blade runner' 
ott_platforms = find_ott_platforms(movie_title)

if ott_platforms:
    print(f'The movie "{movie_title}" is available on the following OTT platforms:')
    for provider in ott_platforms:
        print(f"- {provider['provider_name']}")
else:
    print(f'Sorry, information about "{movie_title}" is not available.')

