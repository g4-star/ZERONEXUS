from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    URLField,
    IntegerField,
    SelectField,
    DateField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    URL,
    NumberRange
)


class CreateProjectForm(FlaskForm):

    title = StringField(
        "Project Title",
        validators=[
            DataRequired()
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired()
        ]
    )

    github_url = URLField(
        "GitHub Repository",
        validators=[
            Optional(),
            URL()
        ]
    )

    demo_url = URLField(
        "Live Demo",
        validators=[
            Optional(),
            URL()
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
        default="Planning"
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("Low", "Low"),
            ("Medium", "Medium"),
            ("High", "High"),
            ("Critical", "Critical")
        ],
        default="Medium"
    )

    progress = IntegerField(
        "Progress (%)",
        default=0,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=100
            )
        ]
    )

    deadline = DateField(
        "Deadline",
        format="%Y-%m-%d",
        validators=[
            Optional()
        ]
    )

    submit = SubmitField(
        "Save Project"
    )
class CreateMeetingForm(FlaskForm):
    
    title = StringField(
        "Meeting Title",
        validators=[
            DataRequired()
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired()
        ]
    )

    meeting_date = DateField(
        "Meeting Date",
        validators=[
            DataRequired()
        ]
    )

    meeting_time = StringField(
        "Meeting Time",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Save Meeting"
    )