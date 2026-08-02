from flask import session, abort
from flask_login import current_user

from app.models import Team


def get_active_team():
    """
    Returns the team currently being viewed.

    Super Admin:
        Uses the selected team stored in the session.

    Team Lead / Member:
        Uses their assigned team.
    """

    if current_user.role == "super_admin":

        team_id = session.get("active_team_id")

        if not team_id:
            return None

        return Team.query.get(team_id)

    return current_user.team

def require_active_team():
    
    team = get_active_team()

    if team is None:
        abort(404)

    return team