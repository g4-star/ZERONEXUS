from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    DateField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length
)


class ProjectForm(FlaskForm):

    title = StringField(
        "Project Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired()
        ]
    )

    status = SelectField(
        "Status",
        choices=[
            ("Planning", "Planning"),
            ("In Progress", "In Progress"),
            ("Testing", "Testing"),
            ("Completed", "Completed")
        ],
        validators=[
            DataRequired()
        ]
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High"),
            ("Critical", "Critical")
        ],
        validators=[
            DataRequired()
        ]
    )

    deadline = DateField(
        "Deadline",
        format="%Y-%m-%d"
    )

    submit = SubmitField(
        "Save Project"
    )
