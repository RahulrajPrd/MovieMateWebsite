from flask import Flask,render_template,request
import requests
import pickle

key = '6ef8d8bb1c71943c941a87efd2162966'

recommend_movie_key = f'https://api.themoviedb.org/3/search/movie?query=Jack+Reacher&api_key={key}'

app = Flask(__name__)

with open('E:\lang\MOVIE-RECOMMODATION-SYSTEM\MOVIES\Movies\model\movies.pkl', 'rb') as file:
    m = pickle.load(file)

with open("E:/lang/MOVIE-RECOMMODATION-SYSTEM/MOVIES/Movies/model/similarity.pkl","rb") as file:
    similarity = pickle.load(file)

titles = m['title']

def recommendMovie(movieName):
    movie_index = m[m['title'] == movieName].index
    recommended_movies = []

    if len(movie_index) > 0:
        movie_index = m[m['title'] == movieName].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[0:7]
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

    for i in range(0,20):
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
    
    for i in range(0,20):
        path.append((data['results'][i]['poster_path']))
    
    posters = []

    url = 'https://image.tmdb.org/t/p/w500/'

    for i in range(0,20):
        posters.append(url+path[i])
    
    return posters

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


@app.route('/')
@app.route('/home')
def hello_world():
    data = nowPlayingMovies()
    images = getPoster()
    return render_template('home.html',data=data,images=images)
    # return render_template('home.html')

@app.route('/recommend',methods=['POST','GET'])
def recommend():
    user_input = None
    recommendations = []
    movie_details = []
    movie_ = []

    error = True

    if request.method == 'POST':
        user_input = request.form['user_input']

        recommendations = recommendMovie(user_input)

        if (len(recommendations) == 0):
            return render_template("404.html",error=error,user_input=user_input)

        for i in range(0,7):
            movie_details.append(getMovie(recommendations[i]))
            movie_.append(getBanner(recommendations[i]))

    return render_template('recommand.html',user_input = user_input,ans=recommendations,movie_details=movie_details,movie_banner=movie_,
                           suggestions=titles)

if __name__ == "__main__":
    app.run(debug=True)