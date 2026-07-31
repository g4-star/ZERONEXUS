from flask import Blueprint, render_template
from app.models import Team, MemberProfile

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template('main/index.html', teams=teams)

@main_bp.route('/teams')
def teams():
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template('main/teams.html', teams=teams)

@main_bp.route('/teams/<slug>')
def team_detail(slug):
    team = Team.query.filter_by(slug=slug).first_or_404()
    return render_template('main/team_detail.html', team=team)

@main_bp.route('/members/<int:member_id>')
def member_profile(member_id):
    member = MemberProfile.query.get_or_404(member_id)
    return render_template('main/member_profile.html', member=member)