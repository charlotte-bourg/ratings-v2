"""Server for movie ratings app."""

from flask import (Flask, render_template, request,flash,session,redirect)
from model import connect_to_db,db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/movies')
def show_all_movies():

    movies = crud.get_movies()

    return render_template('all_movies.html', movies = movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def show_all_users():

    users = crud.get_users()

    return render_template('all_users.html', users = users)

@app.route('/users', methods = ['POST'])
def create_user():
    
    email = request.form.get("email")
    password = request.form.get("password")

    if not crud.get_user_by_email(email):
        flash("Popcorn time baby!")
        user = crud.create_user(email,password)
        db.session.add(user)
        db.session.commit()
    else:
        flash("Unfortunately someone already used that email ):")
    

    return redirect('/')
    
@app.route('/login', methods = ['POST'])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)
    if user.password == password:
        flash("Logged in!")
        session["user_id"] = user.user_id
    else:
        flash("Wrong password!")
        
    return redirect('/')

@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user = user)

@app.route('/movies/<movie_id>/rate-movie')
def submit_rating(movie_id):

    user_rating = request.args.get("movie-rating")
    current_user = crud.get_user_by_id(session["user_id"])
    movie = crud.get_movie_by_id(movie_id)
    rating = crud.create_rating(current_user, movie, user_rating)
    db.session.add(rating)
    db.session.commit()
    return render_template('movie_details.html', movie = movie)
    
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
