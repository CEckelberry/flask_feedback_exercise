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
