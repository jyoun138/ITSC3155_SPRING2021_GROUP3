from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from wtforms import ValidationError
from models import User
from database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Username', validators=[Length(1, 10)])

    email = StringField('Email',
                        [Email(message='Not a valid email address.'), DataRequired()])

    password = PasswordField('Password',
                             [DataRequired(message="Please enter a password."),
                              EqualTo('confirmPassword', message='Passwords must match')])

    confirmPassword = PasswordField('Confirm Password',
                                    validators=[Length(min=1, max=10)])

    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Username', validators=[Length(1, 10)])

    password = PasswordField('Password', [
        DataRequired(message='Please enter a password.')])

    submit = SubmitField('Submit')


class EventForm(FlaskForm):
    class Meta:
        csrf = False

    title = StringField('Title', validators=[Length(1, 20)])

    eventText = StringField('Event Text', validators=[Length(1, 20)])

    eventDate = DateField('Event Date', format='%Y-%m-%d')

    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    class Meta:
        csrf = False

    comment = TextAreaField('Comment', validators=[Length(min=1)])

    submit = SubmitField('Add Comment')

class FriendForm(FlaskForm):
    class Meta:
        csrf = False

    friendUsername = StringField('Username', validators=[Length(1, 20)])

    submit = SubmitField('Add User')
