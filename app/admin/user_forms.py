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
    # member
    # - Can edit own profile
    # - Can participate in team discussions
    # - Can view team projects
    #
    # team_lead
    # - Manages assigned team
    # - Creates and manages projects
    # - Creates meetings
    # - Posts announcements
    # - Manages team workspace
    # - Cannot add/remove members
    #
    # Note:
    # super_admin is NOT created from this form.
    # It is created manually by the system.
    # ===============================

    role = SelectField(
        "Role",
        choices=[
            ("member", "Member"),
            ("team_lead", "Team Lead")
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