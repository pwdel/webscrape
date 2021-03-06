"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
import email_validator
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)
from wtforms_sqlalchemy.orm import QuerySelectField


class SignupForm(FlaskForm):
    """Sponsor Type User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    organization = StringField(
        'Organization',
        validators=[Optional()]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# admin login form
class AdminLoginForm(FlaskForm):
    """User Log-in Form."""
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


# define user_query in order for QuerySelectField query_factory to work
def user_query():
    return User.query

class DocumentForm(FlaskForm):
    """Create New Document Form."""
    document_name = StringField(
        'Document Name',
        validators=[Optional()]
    )
    document_body = StringField(
        'Document Body',
        validators=[Optional()]
    )
    editorchoice = QuerySelectField(
        query_factory=user_query,
        allow_blank=True,
        get_label='name'
    )
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    """Search Term input Form"""
    search = StringField(
        'Search',
        validators=[Optional()]
    )
    submit = SubmitField('Submit')
