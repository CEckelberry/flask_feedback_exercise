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
from forms import AddUserForm, LoginUserForm

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
    form = AddUserForm()
    return render_template("register.html", form=form)


@app.route("/register", methods=["POST"])
def register():
    """registration post route that redirects to secret"""
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/secret")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET"])
def login():
    """Route to login registered users"""

    form = LoginUserForm()

    return render_template("login.html", form=form)


@app.route("/login", methods=["POST"])
def login():
    """Route to login registered users"""
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            return redirect("/secret")
    else:
        form.username.errors = ["invalid username/password"]
        return render_template("login.html")


@app.route("/secret", methods=["GET"])
def show_secret():
    """page that should only show once you are logged in"""
    return "You made it!"
