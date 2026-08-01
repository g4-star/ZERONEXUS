from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    slug = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    icon = db.Column(
        db.String(20)
    )

    level = db.Column(
        db.String(50)
    )

    duration = db.Column(
        db.String(50)
    )

    published = db.Column(
        db.Boolean,
        default=True
    )

    lessons = db.relationship(
        "Lesson",
        backref="course",
        lazy=True,
        cascade="all, delete-orphan"
    )