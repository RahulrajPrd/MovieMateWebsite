# app.py
from flask import Flask, render_template, request
from movie_recommender import recommendMovie, getMovie, getBanner, nowPlayingMovies, getPoster, pickMe, getPickMeMovie, getLinks

app = Flask(__name__)

from models import titles

@app.route('/')
@app.route('/home')
def hello_world():
    data = nowPlayingMovies()
    images = getPoster()
    links = []
    for i in data:
        links.append(getLinks(i))
    return render_template('home.html', data=data, images=images,links=links)


@app.route('/recommend', methods=['POST', 'GET'])
def recommend():

    user_input = None
    recommendations = []
    movie_details = []
    movie_ = []
    bookings = []

    error = True

    if request.method == 'POST':
        user_input = request.form['user_input']

        recommendations = recommendMovie(user_input)

        if (len(recommendations) == 0):
            return render_template("404.html", error=error, user_input=user_input)

        for i in range(0, 7):
            movie_details.append(getMovie(recommendations[i]))
            movie_.append(getBanner(recommendations[i]))

    return render_template('recommand.html', user_input=user_input, ans=recommendations, movie_details=movie_details,
                           movie_banner=movie_, suggestions=titles)

@app.route('/questions',methods = ['POST','GET'])
def questions():

    Generes = ["Comedy","Action","Drama","Adventure","Crime","Biography","Horror",
           "Animation","Fantasy","Documentary","Mystery","Sci-Fi","Western",
           "Family","Musical","Thriller","Romance"]
    
    user_recommendation = []
    pickMeList = []
    OTTplatforms = []

    if request.method == 'POST':
        # Retrieve user responses from the form
        mood = request.form.get('mood')
        age = request.form.get('age')

        user_ansers = {
            'mood':mood,
            'age':age
        }

        user_recommendation = pickMe(user_ansers)

        for i in range(len(user_recommendation)):
            pickMeList.append(getPickMeMovie(user_recommendation[i]))

    return render_template('questions.html',Generes=Generes,
                           user_recommendation=user_recommendation,
                           pickMeList=pickMeList)

if __name__ == "__main__":
    app.run(debug=True)
