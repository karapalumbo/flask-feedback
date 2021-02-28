from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired("Please add a username")])
    password = PasswordField("Password", validators=[InputRequired("Please add a password")])
    email = StringField("Email", validators=[InputRequired("Please add an email"), Email()])
    first_name = StringField("First Name", validators=[InputRequired("First name can't be blank")])
    last_name = StringField("Last Name", validators=[InputRequired("Last name can't be blank")])


class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Please add a title")])
    content = TextAreaField("Content", validators=[InputRequired("Please add your feedback")])


