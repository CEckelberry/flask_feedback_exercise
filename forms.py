"""forms for user exercise"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, URL, AnyOf, NumberRange


class AddUserForm(FlaskForm):
    """form for adding a user"""

    username = StringField("Username")

    password = PasswordField("Password")

    email = StringField("Email", validators=[Email()])

    first_name = StringField("First Name")

    last_name = StringField("Last Name")


class LoginUserForm(FlaskForm):
    """Form to allow registered users to login"""

    username = StringField("Username")

    password = PasswordField("Password")
