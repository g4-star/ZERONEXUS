from flask import render_template

from flask_login import (
    login_required,
    current_user
)

from . import team_bp



@team_bp.route("/dashboard")
@login_required
def dashboard():


    user = current_user

    team = user.team


    return render_template(
        "team/dashboard.html",
        user=user,
        team=team
    )
