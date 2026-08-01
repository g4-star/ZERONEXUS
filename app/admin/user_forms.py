from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email
)


class CreateUserForm(FlaskForm):

    # ===============================
    # User Information
    # ===============================

    full_name = StringField(
        "Full Name",
        validators=[
            DataRequired()
        ]
    )


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    # ===============================
    # User Role
    #
    # member:
    # - Can edit own profile only
    #
    # team_lead:
    # - Manages assigned team
    # - Creates projects
    # - Creates meetings
    # - Manages team workspace
    # - Cannot add/remove users
    #
    # ===============================

    role = SelectField(
        "Role",
        choices=[
            (
                "member",
                "Member"
            ),
            (
                "team_lead",
                "Team Lead"
            )
        ],
        validators=[
            DataRequired()
        ]
    )


    # ===============================
    # Team Assignment
    # ===============================

    team_id = SelectField(
        "Team",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )


    # ===============================
    # Submit Button
    # ===============================

    submit = SubmitField(
        "Create User"
    )