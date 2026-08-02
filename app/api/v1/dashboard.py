from flask import jsonify
from flask_login import login_required, current_user

from . import api
from app.services.dashboard_service import DashboardService


@api.route("/dashboard")
@login_required
def dashboard():

    data = DashboardService.get_dashboard(current_user)

    return jsonify(data)