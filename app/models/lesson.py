from app.extensions import db


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("courses.id"),
        nullable=False
    )

    lesson_number = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    estimated_time = db.Column(
        db.String(50)
    )

    level = db.Column(
        db.String(50)
    )

    published = db.Column(
        db.Boolean,
        default=True
    )