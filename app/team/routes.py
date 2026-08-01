from flask import (
    render_template,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from app.auth.decorators import (
    member_required
)

from . import team_bp


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


    return render_template(
        "team/dashboard.html",
        user=user,
        team=team
    )


# =====================================================
# TEAM PROJECTS
# =====================================================

@team_bp.route("/projects")
@login_required
@member_required
def projects():

    return render_template(
        "team/projects.html",
        user=current_user,
        team=current_user.team
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

    return render_template(
        "team/announcements.html",
        user=current_user,
        team=current_user.team
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