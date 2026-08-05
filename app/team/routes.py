import os

from werkzeug.utils import secure_filename

from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    session,
    request,
    jsonify,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db, limiter

from app.auth.decorators import (
    member_required,
    team_lead_required
)

from . import team_bp

from .forms import CreateProjectForm
from .announcement_forms import CreateAnnouncementForm
from .message_forms import MessageForm

from app.models import (
    User,
    Team,
    Project,
    Meeting,
    Announcement,
    TeamMessage,
    Notification
)

from app.forms.meeting import MeetingForm
from flask import redirect
from sqlalchemy import or_
from app.models import MeetingParticipant, MeetingTeam


def require_active_team():
    
    # ---------------------------------------
    # Team Lead / Member
    # ---------------------------------------

    if not current_user.is_super_admin:

        if current_user.team is None:
            abort(404)

        return current_user.team

    # ---------------------------------------
    # Super Admin
    # ---------------------------------------

    team_id = session.get("active_team_id")

    # No active team? Use the first available team.
    if team_id is None:

        team = Team.query.order_by(Team.name.asc()).first()

        if team is None:
            abort(404)

        session["active_team_id"] = team.id

        return team

    team = Team.query.get(team_id)

    # Stored team deleted? Pick another one.
    if team is None:

        team = Team.query.order_by(Team.name.asc()).first()

        if team is None:
            abort(404)

        session["active_team_id"] = team.id

    return team


# =====================================================
# TEAM DASHBOARD
# =====================================================

@team_bp.route("/dashboard")
@login_required
@member_required
def dashboard():
    """Render the Team Dashboard."""

    team = require_active_team()

    if team is None:

        flash(
            "You are not assigned to a team.",
            "warning"
        )

        return redirect(
            url_for("main.index")
        )

    # =====================================================
    # MEMBERS
    # =====================================================

    members = (
        User.query
        .filter_by(team_id=team.id)
        .order_by(User.created_at.desc())
        .all()
    )

    recent_members = members[:5]

    member_count = (
        User.query
        .filter_by(team_id=team.id)
        .count()
    )

    # =====================================================
    # PROJECTS
    # =====================================================

    projects = (
        Project.query
        .filter(
            db.or_(
                Project.team_id == team.id,
                Project.visibility == "all_teams"
            )
        )
        .order_by(Project.created_at.desc())
        .all()
    )

    recent_projects = projects[:5]

    project_count = len(projects)

    # =====================================================
    # MEETINGS
    # =====================================================

    meetings = (
        Meeting.query
        .filter_by(team_id=team.id)
        .order_by(
            Meeting.meeting_date.asc(),
            Meeting.meeting_time.asc()
        )
        .all()
    )

    meeting_count = len(meetings)

    # =====================================================
    # ANNOUNCEMENTS
    # =====================================================

    announcements = (
        Announcement.query
        .filter_by(team_id=team.id)
        .order_by(
            Announcement.pinned.desc(),
            Announcement.created_at.desc()
        )
        .all()
    )

    recent_announcements = announcements[:5]

    announcement_count = len(announcements)

    # =====================================================
    # TEAM CHAT
    # =====================================================

    messages = (
        TeamMessage.query
        .filter_by(team_id=team.id)
        .order_by(TeamMessage.created_at.desc())
        .limit(10)
        .all()
    )

    # =====================================================
    # USER NOTIFICATIONS
    # =====================================================

    notifications = (
        Notification.query
        .filter_by(
            user_id=current_user.id,
            is_read=False
        )
        .order_by(Notification.created_at.desc())
        .all()
    )

    notification_count = len(notifications)

    # =====================================================
    # PLACEHOLDERS
    # =====================================================

    tasks = []

    recent_activity = []

    completed_tasks = 0

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "user": current_user,

        "team": team,

        # Members
        "members": members,
        "recent_members": recent_members,
        "member_count": member_count,

        # Projects
        "projects": projects,
        "recent_projects": recent_projects,
        "project_count": project_count,

        # Meetings
        "meetings": meetings,
        "meeting_count": meeting_count,

        # Announcements
        "announcements": announcements,
        "recent_announcements": recent_announcements,
        "announcement_count": announcement_count,

        # Chat
        "messages": messages,

        # Notifications
        "notifications": notifications,
        "notification_count": notification_count,

        # Other
        "tasks": tasks,
        "completed_tasks": completed_tasks,
        "recent_activity": recent_activity

    }

    return render_template(
        "team/dashboard.html",
        **context
    )


# =====================================================
# TEAM PROJECTS
# =====================================================

@team_bp.route("/projects")
@login_required
@member_required
def projects():

    team = require_active_team()

    projects = Project.query.filter(
        db.or_(
            Project.team_id == team.id,
            Project.visibility == "all_teams"
        )
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
@member_required
@limiter.limit("10 per minute")
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

            visibility="team",

            team_id=current_user.team.id,

            created_by=current_user.id
        )

        # ============================
        # ZIP UPLOAD
        # ============================

        uploaded_file = form.project_file.data

        if uploaded_file:

            filename = secure_filename(
                uploaded_file.filename
            )

            upload_folder = os.path.join(

                current_app.root_path,

                "static",

                "uploads",

                "projects"

            )

            os.makedirs(
                upload_folder,
                exist_ok=True
            )

            filepath = os.path.join(
                upload_folder,
                filename
            )

            uploaded_file.save(
                filepath
            )

            project.project_file = (
                "uploads/projects/"
                + filename
            )

            project.file_name = filename

            size = os.path.getsize(
                filepath
            )

            project.file_size = (
                f"{round(size / 1024,2)} KB"
            )

        db.session.add(project)

        db.session.commit()

        flash(
            "Project uploaded successfully.",
            "success"
        )

        return redirect(
            url_for(
                "team.projects"
            )
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

    team = require_active_team()

    if current_user.role == "super_admin":

        meetings = (
            Meeting.query
            .order_by(
                Meeting.meeting_date.asc(),
                Meeting.meeting_time.asc()
            )
            .all()
        )

    else:

        shared_ids = db.session.query(
            MeetingTeam.meeting_id
        ).filter(
            MeetingTeam.team_id == team.id
        )

        meetings = (
            Meeting.query
            .filter(
                or_(

                    Meeting.meeting_scope == "global",

                    Meeting.team_id == team.id,

                    Meeting.id.in_(shared_ids)

                )
            )
            .order_by(
                Meeting.meeting_date.asc(),
                Meeting.meeting_time.asc()
            )
            .all()
        )

    return render_template(
        "team/meetings.html",
        user=current_user,
        team=team,
        meetings=meetings
    )

@team_bp.route(
    "/meetings/create",
    methods=["GET", "POST"]
)
@login_required
@team_lead_required
@limiter.limit("5 per minute")
def create_meeting():

    active_team = require_active_team()

    form = MeetingForm()

    # =====================================================
    # LOAD TEAM CHOICES
    # =====================================================

    teams = Team.query.order_by(Team.name.asc()).all()

    # 0 = All Teams (used only for Global meetings)
    form.team_id.choices = [
        (0, "🌍 All Teams")
    ] + [
        (team.id, team.name)
        for team in teams
    ]

    form.shared_team_ids.choices = [
        (team.id, team.name)
        for team in teams
    ]

    # =====================================================
    # TEAM LEADS CAN ONLY CREATE TEAM MEETINGS
    # =====================================================

    if current_user.is_team_lead:

        form.meeting_scope.data = "team"
        form.team_id.data = active_team.id

    # =====================================================
    # CREATE
    # =====================================================

    if form.validate_on_submit():

        try:

            scope = form.meeting_scope.data

            # ------------------------------------------
            # TEAM LEAD
            # ------------------------------------------

            if current_user.is_team_lead:

                scope = "team"
                host_team = active_team.id

            # ------------------------------------------
            # SUPER ADMIN
            # ------------------------------------------

            else:

                if scope == "team":

                    host_team = (
                        None
                        if form.team_id.data == 0
                        else form.team_id.data
                    )

                elif scope == "shared":

                    host_team = None

                else:

                    host_team = None

            # =====================================================
            # CREATE MEETING
            # =====================================================

            meeting = Meeting(

                title=form.title.data,

                description=form.description.data,

                meeting_date=form.meeting_date.data,

                meeting_time=form.meeting_time.data,

                duration=form.duration.data,

                meet_link=form.meet_link.data,

                status=form.status.data,

                meeting_scope=scope,

                team_id=host_team,

                created_by=current_user.id

            )

            db.session.add(meeting)
            db.session.flush()

            # =====================================================
            # SHARED TEAMS
            # =====================================================

            shared_ids = set()

            if scope == "shared":

                shared_ids = set(form.shared_team_ids.data)

                for team_id in shared_ids:

                    db.session.add(

                        MeetingTeam(
                            meeting_id=meeting.id,
                            team_id=team_id
                        )

                    )

            # =====================================================
            # RECIPIENTS
            # =====================================================

            recipients = {}

            if scope == "team":

                members = User.query.filter_by(
                    team_id=host_team
                ).all()

                for member in members:
                    recipients[member.id] = member

            elif scope == "shared":

                for team_id in shared_ids:

                    members = User.query.filter_by(
                        team_id=team_id
                    ).all()

                    for member in members:
                        recipients[member.id] = member

            else:
                # GLOBAL

                members = User.query.all()

                for member in members:
                    recipients[member.id] = member

            # =====================================================
            # PARTICIPANTS + NOTIFICATIONS
            # =====================================================

            for member in recipients.values():

                db.session.add(

                    MeetingParticipant(
                        meeting_id=meeting.id,
                        user_id=member.id
                    )

                )

                db.session.add(

                    Notification(

                        user_id=member.id,

                        title="📅 New Meeting",

                        message=(
                            f"{current_user.display_name} scheduled "
                            f"'{meeting.title}' on "
                            f"{meeting.meeting_date.strftime('%d %b %Y')} "
                            f"at "
                            f"{meeting.meeting_time.strftime('%I:%M %p')}."
                        ),

                        type="meeting",

                        link=url_for("team.meetings")

                    )

                )

            db.session.commit()

            flash(
                "Meeting created successfully.",
                "success"
            )

            return redirect(
                url_for("team.meetings")
            )

        except Exception as e:

            db.session.rollback()

            current_app.logger.exception(e)

            flash(
                "Failed to create meeting.",
                "danger"
            )

    return render_template(
        "team/create_meeting.html",
        form=form,
        team=active_team
    )

@team_bp.route(
    "/meetings/<int:meeting_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@team_lead_required
def edit_meeting(meeting_id):

    team = require_active_team()

    # ----------------------------------------
    # Load Meeting
    # ----------------------------------------

    if current_user.role == "super_admin":

        meeting = Meeting.query.get_or_404(meeting_id)

    else:

        meeting = Meeting.query.filter_by(
            id=meeting_id,
            team_id=team.id,
            meeting_scope="team"
        ).first_or_404()

    form = MeetingForm(obj=meeting)

    # ----------------------------------------
    # Load Teams
    # ----------------------------------------

    teams = Team.query.order_by(Team.name.asc()).all()

    form.team_id.choices = [
        (t.id, t.name)
        for t in teams
    ]

    form.shared_team_ids.choices = [
        (t.id, t.name)
        for t in teams
    ]

    # ----------------------------------------
    # Team Lead Restrictions
    # ----------------------------------------

    if current_user.role == "team_lead":

        form.meeting_scope.data = "team"
        form.team_id.data = team.id

    # ----------------------------------------
    # Load Existing Shared Teams
    # ----------------------------------------

    if request.method == "GET":

        if meeting.team_id:

            form.team_id.data = meeting.team_id

        if meeting.meeting_scope == "shared":

            form.shared_team_ids.data = [
                item.team_id
                for item in meeting.shared_teams
            ]

    # ----------------------------------------
    # Save Changes
    # ----------------------------------------

    if form.validate_on_submit():

        try:

            meeting.title = form.title.data
            meeting.description = form.description.data
            meeting.meeting_date = form.meeting_date.data
            meeting.meeting_time = form.meeting_time.data
            meeting.duration = form.duration.data
            meeting.meet_link = form.meet_link.data
            meeting.status = form.status.data

            if current_user.role == "super_admin":

                meeting.meeting_scope = form.meeting_scope.data

                if meeting.meeting_scope == "global":

                    meeting.team_id = None

                elif meeting.meeting_scope == "team":

                    meeting.team_id = form.team_id.data

                else:

                    meeting.team_id = None

                # Remove old shared teams

                MeetingTeam.query.filter_by(
                    meeting_id=meeting.id
                ).delete()

                # Add new shared teams

                if meeting.meeting_scope == "shared":

                    for team_id in form.shared_team_ids.data:

                        db.session.add(

                            MeetingTeam(
                                meeting_id=meeting.id,
                                team_id=team_id
                            )

                        )

            db.session.commit()

            flash(
                "Meeting updated successfully.",
                "success"
            )

            return redirect(
                url_for("team.meetings")
            )

        except Exception as e:

            db.session.rollback()

            current_app.logger.exception(e)

            flash(
                "Unable to update meeting.",
                "danger"
            )

    return render_template(
        "team/edit_meeting.html",
        form=form,
        meeting=meeting,
        team=team
    )

@team_bp.route(
    "/meetings/<int:meeting_id>/delete",
    methods=["POST"]
)
@login_required
@team_lead_required
def delete_meeting(meeting_id):

    team = require_active_team()

    if current_user.role == "super_admin":

        meeting = Meeting.query.get_or_404(meeting_id)

    else:

        meeting = Meeting.query.filter_by(
            id=meeting_id,
            team_id=team.id,
            meeting_scope="team"
        ).first_or_404()

    db.session.delete(meeting)

    db.session.commit()

    flash(
        "Meeting deleted successfully.",
        "success"
    )

    return redirect(
        url_for("team.meetings")
    )
    
# =====================================================
# JOIN MEETING
# =====================================================

@team_bp.route("/meetings/<int:meeting_id>/join")
@login_required
@member_required
def join_meeting(meeting_id):

    team = require_active_team()

    meeting = Meeting.query.get_or_404(meeting_id)

    # ---------------------------------------
    # Permission Check
    # ---------------------------------------

    allowed = False

    if current_user.role == "super_admin":

        allowed = True

    elif meeting.meeting_scope == "global":

        allowed = True

    elif meeting.meeting_scope == "team":

        allowed = (
            meeting.team_id == team.id
        )

    elif meeting.meeting_scope == "shared":

        allowed = MeetingTeam.query.filter_by(
            meeting_id=meeting.id,
            team_id=team.id
        ).first() is not None

    if not allowed:

        flash(
            "You are not allowed to join this meeting.",
            "danger"
        )

        return redirect(
            url_for("team.meetings")
        )

    # ---------------------------------------
    # Record Attendance
    # ---------------------------------------

    participant = MeetingParticipant.query.filter_by(
        meeting_id=meeting.id,
        user_id=current_user.id
    ).first()

    if participant is None:

        participant = MeetingParticipant(
            meeting_id=meeting.id,
            user_id=current_user.id
        )

        db.session.add(participant)

        db.session.commit()

    # ---------------------------------------
    # Redirect to Meeting
    # ---------------------------------------

    return redirect(
        meeting.meet_link
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

    team = require_active_team()

    members = User.query.filter_by(team_id=team.id).order_by(User.full_name).all()

    return render_template(
        "team/members.html",
        user=current_user,
        team=team,
        members=members
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
@limiter.limit("30 per minute")
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

    team = require_active_team()

    return render_template(
        "team/profile.html",
        user=current_user,
        team=team
    )


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