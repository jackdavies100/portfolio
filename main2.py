import subprocess
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
# Import your forms from the forms.py
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# For adding profile images to the comment section
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES


# Create a User table for all your registered users
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    # This will act like a list of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    # Parent relationship: "comment_author" refers to the comment_author property in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")


# Create a table for the comments on the blog posts
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    # Child relationship:"users.id" The users refers to the tablename of the User class.
    # "comments" refers to the comments property in the User class.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child Relationship to the BlogPosts
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


with app.app_context():
    db.create_all()


# Create an admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        # Check if user email is already present in the database.
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    return render_template("index.html")


# Add a POST method to be able to post comments


# Use a decorator so only an admin user can create new posts


# Use a decorator so only an admin user can edit a post

# Use a decorator so only an admin user can delete a post


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)

@app.route("/snake")
def snake():
    snake_game_dir = 'snake game'
    subprocess.run(['python', 'main.py', 'food.py', 'scoreboard.py', 'snake.py', 'data.txt'], cwd=snake_game_dir)

    # You can also return a message or redirect the user to another page after executing the Snake game
    return render_template("index.html")

@app.route("/quizzler")
def quizzler():
    quizzler_dir = 'quizzler'
    subprocess.run(['python', 'main.py', 'data.py', 'question_model.py', 'quiz_brain.py', 'ui.py'], cwd=quizzler_dir)

    # You can also return a message or redirect the user to another page after executing the Snake game
    return render_template("index.html")

@app.route("/hand_washing")
def hand_washing():
    website_url = "https://drive.google.com/file/d/1A5FPnWsqxT6hNqTyZqQ27RWQZ-eUjxoX/view?usp=sharing"
    return redirect(website_url)

@app.route("/nobel")
def nobel():
    website_url = "https://drive.google.com/file/d/1LbWfFte5GUGUXg7pPYwKiqQM4XkebgXS/view?usp=sharing"
    return redirect(website_url)

@app.route("/turtle")
def turtle():
    turtle_dir = 'turtle'
    subprocess.run(['python', 'main.py', 'car_manager.py', 'scoreboard.py', 'player.py'], cwd=turtle_dir)

    # You can also return a message or redirect the user to another page after executing the Snake game
    return render_template("index.html")

@app.route("/movies")
def movies():
    snake_game_dir = 'movies'
    subprocess.run(['python', 'main.py', 'food.py', 'scoreboard.py', 'snake.py', 'data.txt'], cwd=snake_game_dir)

    # You can also return a message or redirect the user to another page after executing the Snake game
    return render_template("index.html")

@app.route("/kanye")
def kanye():
    kanye_dir = 'kanye'
    subprocess.run(['python', 'main.py', 'food.py', 'scoreboard.py', 'snake.py', 'data.txt'], cwd=snake_game_dir)

    # You can also return a message or redirect the user to another page after executing the Snake game
    return render_template("index.html")

@app.route("/states")
def states():
    snake_game_dir = 'snake game'
    subprocess.run(['python', 'main.py', 'food.py', 'scoreboard.py', 'snake.py', 'data.txt'], cwd=snake_game_dir)

    # You can also return a message or redirect the user to another page after executing the Snake game
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
