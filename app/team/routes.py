from flask import (
    render_template,
    abort,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from app.auth.decorators import (
    member_required
)

from . import team_bp

from .forms import CreateProjectForm

from app.models import (
    User,
    Project,
    Meeting
)

from .forms import (
    CreateProjectForm,
    CreateMeetingForm
)

def team_lead_required():
    
    if current_user.role != "team_lead":

        abort(403)
        
# =====================================================
# TEAM DASHBOARD
# =====================================================

@team_bp.route("/dashboard")
@login_required
@member_required
def dashboard():

    user = current_user
    team = user.team

    if team is None:

        abort(404)

    members = User.query.filter_by(
        team_id=team.id
    ).all()

    projects = Project.query.filter_by(
        team_id=team.id
    ).all()

    return render_template(
        "team/dashboard.html",
        user=user,
        team=team,
        members=members,
        projects=projects
    )

# =====================================================
# TEAM PROJECTS
# =====================================================

@team_bp.route("/projects")
@login_required
@member_required
def projects():

    team = current_user.team

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
@member_required
def create_project():

    team_lead_required()

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
@member_required
def edit_project(project_id):

    team_lead_required()

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
@member_required
def delete_project(project_id):

    team_lead_required()

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

    announcements = Announcement.query.filter_by(
        team_id=current_user.team_id
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
@team_bp.route(
    "/announcements/create",
    methods=["GET","POST"]
)
@login_required
@member_required
def create_announcement():

    if current_user.role != "team_lead":

        abort(403)

    form = CreateAnnouncementForm()

    if form.validate_on_submit():

        announcement = Announcement(

            title=form.title.data,

            content=form.content.data,

            category=form.category.data,

            pinned=form.pinned.data == "1",

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

    return render_template(
        "team/members.html",
        user=current_user,
        team=current_user.team
    )


# =====================================================
# TEAM MESSAGES
# =====================================================

@team_bp.route("/messages")
@login_required
@member_required
def messages():

    return render_template(
        "team/messages.html",
        user=current_user,
        team=current_user.team
    )