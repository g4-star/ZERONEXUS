from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import (
    AdminUser,
    Team,
    MemberProfile,
    Project,
    ContactMessage
)
from .forms import AdminLoginForm
from .member_forms import AddMemberForm
from .team_forms import EditTeamForm
from app.models import SiteSetting, BlogPost
from app.email import send_member_welcome

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.context_processor
def inject_admin_settings():
    settings = SiteSetting.query.first()
    return {'admin_settings': settings}

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = AdminLoginForm()

    if form.validate_on_submit():
        admin = AdminUser.query.filter_by(username=form.username.data).first()

        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        flash('Invalid credentials.', 'danger')

    return render_template('admin/login.html', form=form)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template(
        'admin/dashboard.html',
        team_count=Team.query.count(),
        member_count=MemberProfile.query.count(),
        project_count=Project.query.count()
    )


@admin_bp.route('/teams')
@login_required
def manage_teams():
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template('admin/teams.html', teams=teams)

@admin_bp.route('/teams/<int:team_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)

    form = EditTeamForm(obj=team)

    if form.validate_on_submit():
        team.name = form.name.data
        team.slug = form.slug.data
        team.short_description = form.short_description.data
        team.description = form.description.data
        team.lead_name = form.lead_name.data
        team.lead_role = form.lead_role.data

        db.session.commit()

        flash('Team updated successfully.', 'success')

        return redirect(url_for('admin.manage_teams'))

    return render_template(
        'admin/edit_team.html',
        form=form,
        team=team
    )
    
@admin_bp.route('/members')
@login_required
def manage_members():
    members = MemberProfile.query.order_by(MemberProfile.full_name.asc()).all()
    teams = Team.query.order_by(Team.name.asc()).all()

    return render_template(
        'admin/members.html',
        members=members,
        teams=teams
    )


@admin_bp.route('/members/add', methods=['GET', 'POST'])
@login_required
def add_member():
    form = AddMemberForm()

    teams = Team.query.order_by(Team.name.asc()).all()
    form.team_id.choices = [(team.id, team.name) for team in teams]

    if form.validate_on_submit():

        member = MemberProfile(
            full_name=form.full_name.data,
            role=form.role.data,
            bio=form.bio.data,
            linkedin_url=form.linkedin_url.data,
            github_url=form.github_url.data,
            portfolio_url=form.portfolio_url.data,
            email=form.email.data,
            whatsapp_number=form.whatsapp_number.data,
            skills=form.skills.data,
            team_id=form.team_id.data
        )

        db.session.add(member)
        db.session.commit()

        # Send welcome email
        try:
            send_member_welcome(member)
            flash(
                'Member added successfully and welcome email sent.',
                'success'
            )
        except Exception as e:
            print(f"Email Error: {e}")
            flash(
                'Member added successfully, but the welcome email could not be sent.',
                'warning'
            )

        return redirect(url_for('admin.manage_members'))

    return render_template(
        'admin/add_member.html',
        form=form
    )
    
@admin_bp.route('/members/<int:member_id>/edit', methods=['GET', 'POST'])
def edit_member(member_id):
    from app.models.member_profile import MemberProfile
    from app.main.forms import MemberProfileForm
    from app.extensions import db
    from flask import flash, redirect, render_template, url_for

    member = MemberProfile.query.get_or_404(member_id)

    form = MemberProfileForm(obj=member)

    if form.validate_on_submit():
        form.populate_obj(member)
        db.session.commit()

        flash('Member updated successfully.', 'success')

        return redirect(url_for('admin.manage_members'))

    return render_template(
        'admin/edit_member.html',
        form=form,
        member=member
    )


@admin_bp.route('/members/<int:member_id>/delete', methods=['POST'])
def delete_member(member_id):
    from app.models.member_profile import MemberProfile
    from app.extensions import db
    from flask import flash, redirect, url_for

    member = MemberProfile.query.get_or_404(member_id)

    db.session.delete(member)
    db.session.commit()

    flash('Member deleted successfully.', 'success')

    return redirect(url_for('admin.manage_members'))
    
@admin_bp.route('/projects')
@login_required
def manage_projects():
    projects = Project.query.order_by(Project.title.asc()).all()

    return render_template(
        'admin/projects.html',
        projects=projects
    )

@admin_bp.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    teams = Team.query.all()

    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            github_url=request.form.get('github_url'),
            live_url=request.form.get('live_url'),
            team_id=request.form.get('team_id')
        )

        db.session.add(project)
        db.session.commit()

        flash('Project added successfully.', 'success')
        return redirect(url_for('admin.manage_projects'))

    return render_template('admin/add_project.html', teams=teams)


@admin_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    teams = Team.query.all()

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.github_url = request.form.get('github_url')
        project.live_url = request.form.get('live_url')
        project.team_id = request.form.get('team_id')

        db.session.commit()

        flash('Project updated successfully.', 'success')
        return redirect(url_for('admin.manage_projects'))

    return render_template(
        'admin/edit_project.html',
        project=project,
        teams=teams
    )


@admin_bp.route('/projects/<int:project_id>/delete')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted.', 'success')

    return redirect(url_for('admin.manage_projects'))


@admin_bp.route('/blog')
@login_required
def manage_blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)


@admin_bp.route('/blog/add', methods=['GET', 'POST'])
@login_required
def add_blog_post():
    if request.method == 'POST':
        post = BlogPost(
            title=request.form.get('title'),
            slug=request.form.get('slug'),
            content=request.form.get('content'),
            is_published=True if request.form.get('is_published') else False
        )

        db.session.add(post)
        db.session.commit()

        flash('Blog post created.', 'success')
        return redirect(url_for('admin.manage_blog'))

    return render_template('admin/add_blog_post.html', post=None)


@admin_bp.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.slug = request.form.get('slug')
        post.content = request.form.get('content')
        post.is_published=True if request.form.get('is_published') else False

        db.session.commit()

        flash('Blog post updated.', 'success')
        return redirect(url_for('admin.manage_blog'))

    return render_template('admin/edit_blog_post.html', post=post)


@admin_bp.route('/blog/<int:post_id>/delete')
@login_required
def delete_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash('Blog post deleted.', 'success')

    return redirect(url_for('admin.manage_blog'))

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = SiteSetting.query.first()

    if not settings:
        settings = SiteSetting()
        db.session.add(settings)
        db.session.commit()

    themes = [
        'cyber-blue', 'midnight', 'emerald', 'sunset', 'ocean',
        'royal-purple', 'crimson', 'golden', 'forest', 'graphite',
        'neon-green', 'ice', 'ruby', 'amber', 'violet',
        'teal', 'indigo', 'rose', 'copper', 'obsidian'
    ]

    if request.method == 'POST':
        print('SETTINGS FORM SUBMITTED')
        print(request.form)

        settings.contact_email = request.form.get('contact_email')
        settings.mode = request.form.get('mode')
        settings.theme_name = request.form.get('theme_name')

        db.session.commit()

        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    return render_template(
        'admin/settings.html',
        settings=settings,
        themes=themes
    )
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin_bp.context_processor
def inject_settings():
    from app.models import SiteSetting

    return {
        "settings": SiteSetting.query.first()
    }
    
# =========================================================
# CONTACT MESSAGES
# =========================================================

@admin_bp.route("/messages")
@login_required
def manage_messages():

    messages = ContactMessage.query.order_by(
        ContactMessage.created_at.desc()
    ).all()

    return render_template(
        "admin/messages.html",
        messages=messages
    )
    
@admin_bp.route("/messages/<int:message_id>")
@login_required
def view_message(message_id):

    message = ContactMessage.query.get_or_404(message_id)

    if not message.is_read:

        message.is_read = True

        db.session.commit()

    return render_template(
        "admin/message_detail.html",
        message=message
    )
    
@admin_bp.route("/messages/<int:message_id>/reply")
@login_required
def reply_message(message_id):

    message = ContactMessage.query.get_or_404(message_id)

    message.is_replied = True

    db.session.commit()

    flash("Message marked as replied.", "success")

    return redirect(url_for("admin.view_message", message_id=message.id))


@admin_bp.route("/messages/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(message_id):

    message = ContactMessage.query.get_or_404(message_id)

    db.session.delete(message)

    db.session.commit()

    flash("Message deleted successfully.", "success")

    return redirect(url_for("admin.manage_messages"))