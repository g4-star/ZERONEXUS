from flask import render_template, request

from . import academy
from app.ai.tutor import ask_nexus_ai
from app.extensions import csrf
from app.models.course import Course
from app.models.lesson import Lesson


@academy.route("/")
def home():
    courses = Course.query.filter_by(
        published=True
    ).all()

    return render_template(
        "academy/academy.html",
        courses=courses
    )


@academy.route("/<course_slug>")
def course(course_slug):

    course = Course.query.filter_by(
        slug=course_slug,
        published=True
    ).first_or_404()

    lessons = Lesson.query.filter_by(
        course_id=course.id,
        published=True
    ).order_by(
        Lesson.lesson_number
    ).all()

    return render_template(
        "academy/course.html",
        course=course,
        lessons=lessons
    )


@academy.route("/<course_slug>/module/<int:lesson_number>")
def lesson(course_slug, lesson_number):

    course = Course.query.filter_by(
        slug=course_slug,
        published=True
    ).first_or_404()

    lesson = Lesson.query.filter_by(
        course_id=course.id,
        lesson_number=lesson_number,
        published=True
    ).first_or_404()

    return render_template(
        "academy/module.html",
        course=course,
        lesson=lesson
    )


@csrf.exempt
@academy.route("/tutor", methods=["GET", "POST"])
def tutor():

    course = request.args.get(
        "course",
        "Python Fundamentals"
    )

    lesson = request.args.get(
        "lesson",
        "General"
    )

    answer = None

    if request.method == "POST":

        question = request.form.get("question")

        if question:

            answer = ask_nexus_ai(
                course,
                lesson,
                question
            )

    return render_template(
        "academy/tutor.html",
        answer=answer,
        course=course,
        lesson=lesson
    )