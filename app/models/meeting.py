from datetime import datetime

from app.extensions import db


class Meeting(db.Model):
    __tablename__ = "meetings"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # DETAILS
    # =====================================================

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    meeting_date = db.Column(
        db.Date,
        nullable=False
    )

    meeting_time = db.Column(
        db.Time,
        nullable=False
    )

    duration = db.Column(
        db.Integer,
        default=60
    )

    meet_link = db.Column(
        db.String(500),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Scheduled"
    )

    # team | shared | global
    meeting_scope = db.Column(
        db.String(20),
        nullable=False,
        default="team"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # FOREIGN KEYS
    # =====================================================

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Nullable for Global meetings
    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=True
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    creator = db.relationship(
        "User",
        back_populates="meetings_created"
    )

    team = db.relationship(
        "Team",
        back_populates="meetings"
    )

    shared_teams = db.relationship(
        "MeetingTeam",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy=True
    )

    participants = db.relationship(
        "MeetingParticipant",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self):
        return (
            f"<Meeting {self.title}>"
        )


# =====================================================
# SHARED TEAMS
# =====================================================

class MeetingTeam(db.Model):
    __tablename__ = "meeting_teams"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    meeting_id = db.Column(
        db.Integer,
        db.ForeignKey("meetings.id"),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    meeting = db.relationship(
        "Meeting",
        back_populates="shared_teams"
    )

    team = db.relationship(
        "Team"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "meeting_id",
            "team_id",
            name="uq_meeting_team"
        ),
    )


# =====================================================
# PARTICIPANTS
# =====================================================

class MeetingParticipant(db.Model):
    __tablename__ = "meeting_participants"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    meeting_id = db.Column(
        db.Integer,
        db.ForeignKey("meetings.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    joined_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    left_at = db.Column(
        db.DateTime,
        nullable=True
    )

    meeting = db.relationship(
        "Meeting",
        back_populates="participants"
    )

    user = db.relationship(
        "User"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "meeting_id",
            "user_id",
            name="uq_meeting_participant"
        ),
    )