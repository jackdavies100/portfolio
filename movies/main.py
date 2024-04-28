from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

API_KEY = "65decb9706165cc4b3e1550b76059350"
API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NWRlY2I5NzA2MTY1Y2M0YjNlMTU1MGI3NjA1OTM1MCIsInN1YiI6IjY1ZjcxMzllMjQyZjk0MDE3ZGNjZTliZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ID3SkI05rDh8t7lAS0GuzX5A8-QuCCDVI-1zOgu_aeg"

URL = "https://api.themoviedb.org/3/search/movie"
INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NWRlY2I5NzA2MTY1Y2M0YjNlMTU1MGI3NjA1OTM1MCIsInN1YiI6IjY1ZjcxMzllMjQyZjk0MDE3ZGNjZTliZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ID3SkI05rDh8t7lAS0GuzX5A8-QuCCDVI-1zOgu_aeg"
}




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///film_list.db"
# initialize the app with the extension
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
  year: Mapped[int] = mapped_column( nullable=False)
  description: Mapped[str] = mapped_column(db.String(255), nullable=False)
  rating: Mapped[float] = mapped_column(db.Float, nullable=True)
  ranking: Mapped[int] = mapped_column(db.Integer, nullable=True)
  review: Mapped[str] = mapped_column(db.String(255), nullable=False)
  img_url: Mapped[str] = mapped_column(db.String(255), nullable=False)


with app.app_context():
    db.create_all()

class MovieForm(FlaskForm):
    rating = StringField('Your rating out fo 10')
    review = StringField("Your Review")
    done = SubmitField('Done')

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    done = SubmitField('Done')

@app.route("/movies")
def movies():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("movies_index.html", movies=all_movies)

@app.route("/movies/edit", methods=["GET", "POST"])
def edit():
    form = MovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)

    if form.validate_on_submit():
        try:
            # Attempt to convert rating to float
            movie.rating = float(form.rating.data)
        except ValueError:
            # If conversion fails, set review field to rating data
            movie.review = form.rating.data
        else:
            # If conversion succeeds, set review field to form review data
            movie.review = form.review.data

        # Commit changes to the database
        db.session.commit()

        # Redirect back to the home page after successful update
        return redirect(url_for('home'))

    # If the form is not submitted or validation fails, render the edit page again
    return render_template("movies_edit.html", movie=movie, form=form)

@app.route("/movies/delete")
def delete():
    movie_id = request.args.get('id')

    # DELETE A RECORD BY ID
    movie_to_delete = db.get_or_404(Movie, movie_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/movies/add", methods = ['GET', 'POST'])
def add():
    form = FindMovieForm()

    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(URL, params={"api_key": API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("movies_select.html", options=data)

    return render_template("movies_add.html", form=form)

@app.route("/movies/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        data = response.json()
        # Check if the API response contains a non-NULL value for the description field
        if "overview" in data and data["overview"]:
            description = data["overview"]
        else:
            description = "No description available"
        num_movies = db.session.query(func.count(Movie.id)).scalar()
        ranking = num_movies + 1
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_IMAGE_URL}{data['poster_path']}",
            description=description,
            ranking=ranking,
            review = "No review available"
        )
        db.session.add(new_movie)
        db.session.commit()

        # Redirect to /edit route
        return redirect(url_for("movies/edit", id=new_movie.id))



if __name__ == '__main__':
    app.run(debug=True, port=5005)

print(response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
)