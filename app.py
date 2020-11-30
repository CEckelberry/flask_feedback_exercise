from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    render_template,
    jsonify,
    request,
)
from models import db, connect_db, User

app = Flask(__name__)

app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)


@app.route("/", methods=["GET"])
def root_redir_page():
    """redirects to /register"""
    return redirect("/register")


@app.route("/register", methods=["GET"])
def register():
    """registration page for a new user"""
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    """registration post route that redirects to secret"""
    return redirect("/secret")


@app.route("/login", methods=["GET"])
def login():
    """Route to login registered users"""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Route to login registered users"""
    return redirect("/secret")


@app.route("/secret", methods=["GET"])
def show_secret():
    """page that should only show once you are logged in"""
    return "You made it!"
