from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    DateField,
    TimeField,
    IntegerField,
    URLField,
    SubmitField,
    SelectField,
    SelectMultipleField
)

from wtforms.validators import (
    DataRequired,
    Length,
    URL,
    NumberRange,
    Optional
)


class MeetingForm(FlaskForm):

    # =====================================================
    # Basic Information
    # =====================================================

    title = StringField(
        "Meeting Title",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired()
        ]
    )

    # =====================================================
    # Schedule
    # =====================================================

    meeting_date = DateField(
        "Meeting Date",
        validators=[
            DataRequired()
        ]
    )

    meeting_time = TimeField(
        "Meeting Time",
        validators=[
            DataRequired()
        ]
    )

    duration = IntegerField(
        "Duration (Minutes)",
        default=60,
        validators=[
            DataRequired(),
            NumberRange(
                min=5,
                max=600
            )
        ]
    )

    # =====================================================
    # Meeting Link
    # =====================================================

    meet_link = URLField(
        "Meeting Link",
        validators=[
            DataRequired(),
            URL()
        ]
    )

    # =====================================================
    # Meeting Scope
    # =====================================================

    meeting_scope = SelectField(
        "Meeting Type",
        validators=[
            DataRequired()
        ],
        choices=[
            ("team", "Team Meeting"),
            ("shared", "Shared Meeting"),
            ("global", "Global Meeting")
        ],
        default="team"
    )

    # =====================================================
    # Team Selection
    #
    # 0 = All Teams
    # >0 = Actual Team ID
    # =====================================================

    team_id = SelectField(
        "Team",
        coerce=int,
        validators=[
            Optional()
        ],
        choices=[
            (0, "All Teams")
        ],
        default=0,
        validate_choice=False
    )

    # =====================================================
    # Shared Teams
    # =====================================================

    shared_team_ids = SelectMultipleField(
        "Shared Teams",
        coerce=int,
        validators=[
            Optional()
        ],
        choices=[],
        validate_choice=False
    )

    # =====================================================
    # Status
    # =====================================================

    status = SelectField(
        "Status",
        validators=[
            DataRequired()
        ],
        choices=[
            ("Scheduled", "Scheduled"),
            ("Live", "Live"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled")
        ],
        default="Scheduled"
    )

    # =====================================================
    # Submit
    # =====================================================

    submit = SubmitField(
        "Create Meeting"
    )