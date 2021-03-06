from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """connect to the database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Simple user Model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<Username: {self.username} Email: {self.email} first_name: {self.first_name} last_name: {self.last_name}>"

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """register user and created hashed pwd"""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8)
        hashed_utf8 = hashed.decode("utf8")

        # return instace of user with username and hashed pwd
        return cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate a user exists and that the password is correct
        It will return a user if valid, otherwise will return false"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback Model"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String(20), db.ForeignKey("users.username"))
