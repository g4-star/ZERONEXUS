from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length
)


class LoginForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField(
        "Login"
    )



class ActivateAccountForm(FlaskForm):

    password = PasswordField(
        "Create New Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                message="Password must be at least 8 characters"
            )
        ]
    )


    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match"
            )
        ]
    )


    submit = SubmitField(
        "Activate Account"
    )
