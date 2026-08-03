from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    session,
    request
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.auth.decorators import (
    member_required,
    team_lead_required
)

from . import team_bp

from .forms import (
    CreateProjectForm,
    CreateMeetingForm
)

from .announcement_forms import CreateAnnouncementForm

from app.models import (
    User,
    Team,
    Project,
    Meeting,
    Announcement,
    TeamMessage
)
from .message_forms import MessageForm
from flask import redirect, url_for
from flask import render_template
from flask_login import current_user, login_required
from app.models import Team, User, Project
from app.models import TeamMessage
from flask import jsonify

def require_active_team():

    # Team Lead / Member
    if current_user.role != "super_admin":

        if current_user.team is None:
            abort(404)

        return current_user.team

    # Super Admin
    team_id = session.get("active_team_id")

    if not team_id:
        abort(404)

    team = Team.query.get(team_id)

    if team is None:
        abort(404)

    return team


# =====================================================
# TEAM DASHBOARD
# =====================================================

@team_bp.route("/dashboard")
@login_required
@member_required
def dashboard():

    user = current_user

    team = require_active_team()

    members = User.query.filter_by(
        team_id=team.id
    ).order_by(
        User.created_at.desc()
    ).all()

    recent_members = members[:5]

    projects = Project.query.filter_by(
        team_id=team.id
    ).order_by(
        Project.created_at.desc()
    ).all()

    meetings = Meeting.query.filter_by(
        team_id=team.id
    ).all()

    announcements = Announcement.query.filter_by(
        team_id=team.id
    ).order_by(
        Announcement.pinned.desc(),
        Announcement.created_at.desc()
    ).all()

    return render_template(
        "team/dashboard.html",

        user=user,

        team=team,

        members=members,
        recent_members=recent_members,

        projects=projects,

        meetings=meetings,

        announcements=announcements,

        member_count=len(members),

        project_count=len(projects),

        meeting_count=len(meetings),

        announcement_count=len(announcements)
    )


# =====================================================
# TEAM PROJECTS
# =====================================================

@team_bp.route("/projects")
@login_required
@member_required
def projects():

    team = current_user.team

    if team is None:
        abort(404)

    projects = Project.query.filter_by(
        team_id=team.id
    ).order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "team/projects.html",
        user=current_user,
        team=team,
        projects=projects
    )


# =====================================================
# CREATE PROJECT
# =====================================================

@team_bp.route(
    "/projects/create",
    methods=["GET", "POST"]
)
@login_required
@team_lead_required
def create_project():

    if current_user.team is None:
        abort(404)

    form = CreateProjectForm()

    if form.validate_on_submit():

        project = Project(
            title=form.title.data,
            description=form.description.data,
            github_url=form.github_url.data,
            demo_url=form.demo_url.data,
            status=form.status.data,
            priority=form.priority.data,
            progress=form.progress.data,
            deadline=form.deadline.data,
            team_id=current_user.team.id,
            created_by=current_user.id
        )

        db.session.add(project)
        db.session.commit()

        flash(
            "Project created successfully.",
            "success"
        )

        return redirect(
            url_for("team.projects")
        )

    return render_template(
        "team/create_project.html",
        form=form
    )


# =====================================================
# EDIT PROJECT
# =====================================================

@team_bp.route(
    "/projects/<int:project_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@team_lead_required
def edit_project(project_id):

    if current_user.team is None:
        abort(404)

    project = Project.query.filter_by(
        id=project_id,
        team_id=current_user.team.id
    ).first_or_404()

    form = CreateProjectForm(obj=project)

    if form.validate_on_submit():

        project.title = form.title.data
        project.description = form.description.data
        project.github_url = form.github_url.data
        project.demo_url = form.demo_url.data
        project.status = form.status.data
        project.priority = form.priority.data
        project.progress = form.progress.data
        project.deadline = form.deadline.data

        db.session.commit()

        flash(
            "Project updated successfully.",
            "success"
        )

        return redirect(
            url_for("team.projects")
        )

    return render_template(
        "team/edit_project.html",
        form=form,
        project=project
    )


# =====================================================
# DELETE PROJECT
# =====================================================

@team_bp.route(
    "/projects/<int:project_id>/delete"
)
@login_required
@team_lead_required
def delete_project(project_id):

    if current_user.team is None:
        abort(404)

    project = Project.query.filter_by(
        id=project_id,
        team_id=current_user.team.id
    ).first_or_404()

    db.session.delete(project)
    db.session.commit()

    flash(
        "Project deleted successfully.",
        "success"
    )

    return redirect(
        url_for("team.projects")
    )


# =====================================================
# TEAM MEETINGS
# =====================================================

@team_bp.route("/meetings")
@login_required
@member_required
def meetings():

    return render_template(
        "team/meetings.html",
        user=current_user,
        team=current_user.team
    )


# =====================================================
# TEAM ANNOUNCEMENTS
# =====================================================

@team_bp.route("/announcements")
@login_required
@member_required
def announcements():

    if current_user.team is None:
        abort(404)

    announcements = Announcement.query.filter_by(
        team_id=current_user.team.id
    ).order_by(
        Announcement.pinned.desc(),
        Announcement.created_at.desc()
    ).all()

    return render_template(
        "team/announcements.html",
        announcements=announcements,
        user=current_user,
        team=current_user.team
    )


# =====================================================
# CREATE ANNOUNCEMENT
# =====================================================

@team_bp.route(
    "/announcements/create",
    methods=["GET", "POST"]
)
@login_required
@team_lead_required
def create_announcement():

    if current_user.team is None:
        abort(404)

    form = CreateAnnouncementForm()

    if form.validate_on_submit():

        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            pinned=form.pinned.data,
            team=current_user.team,
            author=current_user
        )

        db.session.add(announcement)
        db.session.commit()

        flash(
            "Announcement published.",
            "success"
        )

        return redirect(
            url_for("team.announcements")
        )

    return render_template(
        "team/create_announcement.html",
        form=form
    )


# =====================================================
# TEAM MEMBERS
# =====================================================

@team_bp.route("/members")
@login_required
@member_required
def members():

    if current_user.team is None:
        abort(404)

    return render_template(
        "team/members.html",
        user=current_user,
        team=current_user.team
    )



    # =====================================================
# TEAM CHAT
# =====================================================

@team_bp.route("/messages", methods=["GET", "POST"])
@login_required
@member_required
def messages():

    team = require_active_team()

    form = MessageForm()

    if form.validate_on_submit():

        message = TeamMessage(
            message=form.message.data,
            team_id=team.id,
            user_id=current_user.id
        )

        db.session.add(message)
        db.session.commit()

        flash("Message sent.", "success")

        return redirect(url_for("team.messages"))

    messages = (
        TeamMessage.query
        .filter_by(team_id=team.id)
        .order_by(TeamMessage.created_at.asc())
        .all()
    )

    return render_template(
        "team/messages.html",
        form=form,
        team=team,
        messages=messages
    )


# =====================================================
# DASHBOARD CHAT SEND
# =====================================================

@team_bp.route("/chat/send", methods=["POST"])
@login_required
@member_required
def send_chat():

    team = require_active_team()

    # Support JSON and HTML forms
    if request.is_json:
        data = request.get_json()
        text = (data.get("message") or "").strip()
    else:
        text = request.form.get("message", "").strip()

    if not text:

        if request.is_json:
            return jsonify({
                "ok": False,
                "error": "Empty message"
            }), 400

        return redirect(url_for("team.dashboard"))

    chat = TeamMessage(
        message=text,
        team_id=team.id,
        user_id=current_user.id
    )

    db.session.add(chat)
    db.session.commit()

    # JavaScript request
    if request.is_json:

        return jsonify({
            "ok": True,
            "message": {
                "id": chat.id,
                "author": current_user.username,
                "message": chat.message,
                "time": chat.created_at.strftime("%H:%M")
            }
        })

    # Normal HTML form
    return redirect(url_for("team.dashboard"))


# =====================================================
# CHAT HISTORY API
# =====================================================

@team_bp.route("/messages/api")
@login_required
@member_required
def messages_api():

    team = require_active_team()

    messages = (
        TeamMessage.query
        .filter_by(team_id=team.id)
        .order_by(TeamMessage.created_at.asc())
        .all()
    )

    return jsonify([
        {
            "id": m.id,
            "author": m.author.username,
            "message": m.message,
            "time": m.created_at.strftime("%H:%M")
        }
        for m in messages
    ])

# =====================================================
# TEAM PROFILE
# =====================================================

@team_bp.route("/profile")
@login_required
@member_required
def profile():
    return redirect(url_for("team.dashboard"))
    
# =====================================================
# TEAM TASKS
# =====================================================

@team_bp.route("/tasks")
@login_required
@member_required
def tasks():

    team = require_active_team()

    return render_template(
        "team/tasks.html",
        user=current_user,
        team=team
    )


# =====================================================
# TEAM REPORTS
# =====================================================

@team_bp.route("/reports")
@login_required
@member_required
def reports():

    team = require_active_team()

    return render_template(
        "team/reports.html",
        user=current_user,
        team=team
    )


# =====================================================
# TEAM SETTINGS
# =====================================================

@team_bp.route("/settings")
@login_required
@member_required
def settings():

    team = require_active_team()

    return render_template(
        "team/settings.html",
        user=current_user,
        team=team
    )