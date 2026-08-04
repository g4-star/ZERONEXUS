from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    URLField,
    IntegerField,
    SelectField,
    DateField,
    SubmitField,
    FileField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    URL,
    NumberRange
)

from flask_wtf.file import FileAllowed


# =====================================================
# CREATE PROJECT FORM
# =====================================================

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


    # ===============================
    # ZIP FILE UPLOAD
    # ===============================

    project_file = FileField(
        "Project ZIP File",
        validators=[
            Optional(),
            FileAllowed(
                [
                    "zip"
                ],
                "Only ZIP files are allowed."
            )
        ]
    )


    # ===============================
    # LINKS
    # ===============================

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


    # ===============================
    # VISIBILITY
    # ===============================

    visibility = SelectField(
        "Project Visibility",
        choices=[
            (
                "team",
                "Only My Team"
            ),
            (
                "all_teams",
                "All Teams"
            )
        ],
        default="team"
    )


    # ===============================
    # PROJECT STATUS
    # ===============================

    status = SelectField(
        "Status",
        choices=[
            (
                "Planning",
                "Planning"
            ),
            (
                "In Progress",
                "In Progress"
            ),
            (
                "Testing",
                "Testing"
            ),
            (
                "Completed",
                "Completed"
            )
        ],
        default="Planning"
    )


    priority = SelectField(
        "Priority",
        choices=[
            (
                "Low",
                "Low"
            ),
            (
                "Medium",
                "Medium"
            ),
            (
                "High",
                "High"
            ),
            (
                "Critical",
                "Critical"
            )
        ],
        default="Medium"
    )


    progress = IntegerField(
        "Progress (%)",
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                max=100
            )
        ],
        default=0
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



# =====================================================
# CREATE MEETING FORM
# =====================================================

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