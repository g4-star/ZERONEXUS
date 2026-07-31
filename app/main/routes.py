from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app
)
from app.models import Team, MemberProfile
from app.main.forms import MemberProfileForm
from app.extensions import db

import os
from werkzeug.utils import secure_filename


main_bp = Blueprint('main', __name__)


# -------------------------------------------------
# Home Page
# -------------------------------------------------
@main_bp.route('/')
def index():
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template('main/index.html', teams=teams)


# -------------------------------------------------
# Teams Page
# -------------------------------------------------
@main_bp.route('/teams')
def teams():
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template('main/teams.html', teams=teams)


# -------------------------------------------------
# Team Detail
# -------------------------------------------------
@main_bp.route('/teams/<slug>')
def team_detail(slug):
    team = Team.query.filter_by(slug=slug).first_or_404()
    return render_template('main/team_detail.html', team=team)


# -------------------------------------------------
# Public Member Profile
# -------------------------------------------------
@main_bp.route('/members/<int:member_id>')
def member_profile(member_id):
    member = MemberProfile.query.get_or_404(member_id)
    return render_template('main/member_profile.html', member=member)


# -------------------------------------------------
# Private Member Edit Link
# -------------------------------------------------
@main_bp.route('/member/edit/<token>', methods=['GET', 'POST'])
def edit_member(token):

    member = MemberProfile.query.filter_by(
        profile_token=token
    ).first_or_404()

    form = MemberProfileForm(obj=member)

    if form.validate_on_submit():

        # Skip file upload on Vercel (read-only filesystem)

        member.full_name = form.full_name.data
        member.role = form.role.data
        member.bio = form.bio.data
        member.linkedin_url = form.linkedin_url.data
        member.github_url = form.github_url.data
        member.portfolio_url = form.portfolio_url.data
        member.email = form.email.data
        member.whatsapp_number = form.whatsapp_number.data
        member.skills = form.skills.data

        db.session.commit()

        flash(
            'Your profile has been updated successfully.',
            'success'
        )

        # Redirect user to homepage after saving
        return redirect(url_for('main.index'))

    return render_template(
        'main/edit_member.html',
        form=form,
        member=member
    )