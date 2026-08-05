from flask import render_template, request, redirect, url_for, flash

from flask_login import login_required, current_user

from . import academy
from app.ai.tutor import ask_nexus_ai
from app.extensions import csrf, db, limiter

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.progress import UserProgress

# Category keyword rules (priority order matters: check Cyber before Web)
CATEGORY_RULES = [
    ("Cybersecurity",       ("cyber", "security", "linux", "network", "hack", "forensic", "soc")),
    ("Web Development",     ("html", "css", "javascript", "web")),
    ("Artificial Intelligence", ("ai", "machine", "neural", "intelligence", "data science")),
    ("Python Programming",  ("python",)),
]


def course_category(course):
    """Derive a category from title/slug — works until you add a real column."""
    if getattr(course, "category", None):          # use the real column if you add it later
        return course.category
    text = f"{course.title} {course.slug}".lower()
    for label, keywords in CATEGORY_RULES:
        if any(k in text for k in keywords):
            return label
    return "Other"


@academy.route("/")
def home():
    cat_param = request.args.get("category", "").strip()
    active = "All" if cat_param.lower() in ("", "all") else cat_param

    courses = Course.query.filter_by(published=True).order_by(Course.id).all()

    # One query for all published lessons, grouped by course (no N+1)
    lessons_by_course = {}
    for lesson in Lesson.query.filter_by(published=True).order_by(Lesson.lesson_number).all():
        lessons_by_course.setdefault(lesson.course_id, []).append(lesson)

    # One query for the member's progress
    progress_by_course = {}
    if current_user.is_authenticated:
        completed_ids = {
            p.lesson_id for p in UserProgress.query.filter_by(
                user_id=current_user.id, completed=True
            ).all()
        }
        for course_id, ls in lessons_by_course.items():
            done = sum(1 for l in ls if l.id in completed_ids)
            progress_by_course[course_id] = round(done / len(ls) * 100) if ls else 0

    # Category filter
    labeled = [(c, course_category(c)) for c in courses]
    categories = []
    for _, label in labeled:
        if label not in categories:
            categories.append(label)

    if active != "All":
        labeled = [(c, l) for c, l in labeled if l.lower() == active.lower()]

    return render_template(
        "academy/academy.html",
        courses=[c for c, _ in labeled],
        categories=categories,
        active_category=active,
        lessons_by_course=lessons_by_course,
        progress_by_course=progress_by_course,
    )


@academy.route("/<course_slug>")
def course(course_slug):
    course = Course.query.filter_by(slug=course_slug, published=True).first_or_404()

    lessons = Lesson.query.filter_by(course_id=course.id, published=True).order_by(
        Lesson.lesson_number
    ).all()

    return render_template("academy/course.html", course=course, lessons=lessons)


@academy.route("/<course_slug>/module/<int:lesson_number>")
def lesson(course_slug, lesson_number):
    course = Course.query.filter_by(slug=course_slug, published=True).first_or_404()
    lesson = Lesson.query.filter_by(
        course_id=course.id, lesson_number=lesson_number, published=True
    ).first_or_404()

    completed = False
    progress_percent = 0

    if current_user.is_authenticated:
        rows = UserProgress.query.filter_by(user_id=current_user.id).all()
        completed_ids = {r.lesson_id for r in rows if r.completed}
        completed = lesson.id in completed_ids
        total = len(course.lessons)
        done = sum(1 for l in course.lessons if l.id in completed_ids)
        progress_percent = round(done / total * 100) if total else 0

    return render_template(
        "academy/module.html",
        course=course,
        lesson=lesson,
        completed=completed,
        progress_percent=progress_percent,
    )


@academy.route("/lesson/<int:lesson_id>/complete", methods=["POST"])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)

    progress = UserProgress.query.filter_by(
        user_id=current_user.id, lesson_id=lesson_id
    ).first()

    if progress is None:
        progress = UserProgress(user_id=current_user.id, lesson_id=lesson_id, completed=True)
        db.session.add(progress)
    else:
        progress.completed = True

    db.session.commit()
    flash("✅ Lesson completed!", "success")

    course = Course.query.get(lesson.course_id)
    return redirect(url_for("academy.lesson",
                            course_slug=course.slug,
                            lesson_number=lesson.lesson_number))


@academy.route("/tutor", methods=["GET", "POST"])
@limiter.limit("20 per minute")
def tutor():
    course_title = request.form.get("course") or request.args.get("course")
    lesson_title = request.form.get("lesson") or request.args.get("lesson")
    course_slug = request.form.get("course_slug") or request.args.get("course_slug")

    # Resolve the real Course object: slug first, then title, then default
    course = None
    if course_slug:
        course = Course.query.filter_by(slug=course_slug, published=True).first()
    if course is None and course_title:
        course = Course.query.filter_by(title=course_title, published=True).first()

    course_name = course.title if course else (course_title or "Python Fundamentals")
    lesson_name = lesson_title or "General"

    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            answer = ask_nexus_ai(course_name, lesson_name, question)

    return render_template(
        "academy/tutor.html",
        answer=answer,
        course=course_name,
        lesson=lesson_name,
        course_slug=course.slug if course else course_slug,
    )