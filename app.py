from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    render_template,
    jsonify,
    request,
    session,
)
from models import db, connect_db, User, Feedback
from forms import AddUserForm, LoginUserForm, FeedbackForm
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "oh-so-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)
db.create_all()


@app.route("/", methods=["GET"])
def root_redir_page():
    """redirects to /register"""
    return redirect("/register")


@app.route("/register", methods=["GET", "DELETE"])
def register():
    """registration page for a new user"""
    form = AddUserForm()
    return render_template("register.html", form=form)


@app.route("/register", methods=["POST"])
def register_post():
    """registration post route that redirects to secret"""
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET"])
def login():
    """Route to login registered users"""

    form = LoginUserForm()

    return render_template("login.html", form=form)


@app.route("/login", methods=["POST"])
def login_post():
    """Route to login registered users"""
    form = LoginUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")
    else:
        form.username.errors = ["invalid username/password"]
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
def logout():
    """This route clears out session data and logs a user out"""
    session.clear()
    return redirect("/")


@app.route("/users/<username>", methods=["GET", "DELETE"])
def show_profile(username):
    """page that should only show once you are logged in"""
    user = User.query.get_or_404(username)
    feedback = Feedback.query.filter_by(username=username)
    print(user)
    # email = user["email"]
    # first_name = user["first_name"]
    # last_name = user["last_name"]
    if "username" not in session:
        flash("Please login before attempting to view the secret!", "error")
        return redirect("/login")

    return render_template("user.html", user=user, feedback=feedback)


@app.route("/users/<username>/delete", methods=["DELETE"])
def delete_profile(username):
    """route to delete a user"""
    user = User.query.get_or_404(username)
    if "username" not in session:
        flash("Please login before attempting to view this page!", "error")
        return redirect("/login")

    db.session.delete(user)
    db.session.commit()

    return redirect("/register")


@app.route("/users/<username>/feedback/add", methods=["GET"])
def add_feedback(username):
    """form to add user feedback and tie it to a user account"""
    user = User.query.get_or_404(username)
    form = FeedbackForm()

    if "username" not in session:
        flash("Please login before attempting to view this page!", "error")
        return redirect("/login")

    return render_template("feedback_form.html", user=user, form=form)


@app.route("/users/<username>/feedback/add", methods=["POST"])
def add_feedback_sub(username):
    """submission POST route for feedback"""
    user = User.query.get_or_404(username)
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        username = user.username
        if user:
            session["username"] = user.username
            new_feedback = Feedback(title=title, content=content, username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f"/users/{username}")

        else:
            form.username.errors = ["both fields require input"]
            return render_template("feedback_form.html")


@app.route("/feedback/<feedback_id>/update", methods=["GET"])
def edit_feedback(feedback_id):
    """Edit feedback form with pre-populated fields"""
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if "username" not in session:
        flash("Please login before attempting to view this page!", "error")
        return redirect("/login")

    return render_template("feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<feedback_id>/update", methods=["POST"])
def edit_feedback_sub(feedback_id):
    """Edit feedback POST/submission route"""
    username = session["username"]
    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{username}")


@app.route("/feedback/<feedback_id>/delete", methods=["DELETE"])
def delete_feedback(feedback_id):
    """Delete a single feedback instance by ID"""
    username = session["username"]
    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session:
        flash("Please login before attempting to perform a delete action", "error")
        return redirect("/login")

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{username}")
