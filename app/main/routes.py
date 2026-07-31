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

@main_bp.route('/member/edit/<token>', methods=['GET', 'POST'])
def edit_member(token):
    from app.models.member_profile import MemberProfile
    from app.main.forms import MemberProfileForm
    from app.extensions import db
    from flask import flash, redirect, render_template, url_for

    member = MemberProfile.query.filter_by(
        profile_token=token
    ).first_or_404()

    form = MemberProfileForm(obj=member)

    if form.validate_on_submit():
        form.populate_obj(member)
        db.session.commit()

        flash(
            'Your profile has been updated successfully.',
            'success'
        )

        return redirect(
            url_for('main.edit_member', token=token)
        )

    return render_template(
        'main/edit_member.html',
        form=form,
        member=member
    )