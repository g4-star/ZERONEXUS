from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.admin_user import AdminUser
from app.extensions import db
from app.models import (
    Team,
    MemberProfile,
    Project,
    SiteSetting,
    BlogPost,
    ContactMessage,
    Announcement,
    User
)

from .forms import AdminLoginForm
from .member_forms import AddMemberForm
from .user_forms import CreateUserForm
from .team_forms import EditTeamForm
from .announcement_forms import CreateAnnouncementForm

from app.email import (
    send_member_welcome,
    send_member_invitation
)

from app.utils.permissions import (
    super_admin_required
)
from flask import session
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    session
)
from app.auth.decorators import (
    super_admin_required
)
import os

from werkzeug.utils import secure_filename

from app.models import Project, Team
from app.cloudinary_config import upload_project_file

from flask import current_app
import secrets
import string


# ==========================================
# Admin Blueprint
# ==========================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


def generate_temp_password():
    """Generate a temporary password for invited users."""

    chars = string.ascii_letters + string.digits

    return "ZN@" + "".join(
        secrets.choice(chars)
        for _ in range(8)
    )


def generate_username(full_name):
    """
    Generate a unique username from a user's full name.

    Example:
        John Doe  -> johndoe
        John Doe  -> johndoe1
        John Doe  -> johndoe2
    """

    base_username = (
        full_name.strip()
        .lower()
        .replace(" ", "")
    )

    username = base_username
    counter = 1

    while User.query.filter_by(username=username).first():
        username = f"{base_username}{counter}"
        counter += 1

    return username

@admin_bp.context_processor
def inject_admin_settings():
    settings = SiteSetting.query.first()
    return {'admin_settings': settings}

from sqlalchemy import or_


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "super_admin":
            return redirect(url_for("admin.dashboard"))

        elif current_user.role in ("team_admin", "team_lead"):
            return redirect(url_for("team.dashboard"))

        return redirect(url_for("user.profile"))

    form = AdminLoginForm()

    if form.validate_on_submit():

        admin = User.query.filter(
            or_(
                User.username == form.username.data,
                User.email == form.username.data
            ),
        ).first()

        if admin and admin.check_password(form.password.data):

            login_user(admin)

            flash(
                "Welcome back.",
                "success"
            )

            return redirect(
                url_for("admin.dashboard")
            )

        flash(
            "Invalid credentials.",
            "danger"
        )

    return render_template(
        "admin/login.html",
        form=form
    )
    

# =====================================================
# ADMIN DASHBOARD
# =====================================================

@admin_bp.route("/dashboard")
@login_required
@super_admin_required
def dashboard():

    return render_template(
        "admin/dashboard.html",
        team_count=Team.query.count(),
        member_count=MemberProfile.query.count(),
        project_count=Project.query.count()
    )

# =====================================================
# CREATE TEAM
# =====================================================

@admin_bp.route("/teams/create", methods=["GET", "POST"])
@login_required
@super_admin_required
def create_team():

    return render_template(
        "admin/create_team.html"
    )
# =====================================================
# MANAGE TEAMS
# =====================================================

@admin_bp.route("/teams")
@login_required
@super_admin_required
def manage_teams():

    teams = Team.query.order_by(
        Team.name.asc()
    ).all()

    return render_template(
        "admin/teams.html",
        teams=teams
    )


# =====================================================
# OPEN TEAM WORKSPACE
# =====================================================

@admin_bp.route("/teams/<int:team_id>/open")
@login_required
@super_admin_required
def open_team(team_id):

    from flask import session

    team = db.session.get(Team, team_id)

    if team is None:
        abort(404)

    session["active_team_id"] = team.id

    flash(
        f"You are now managing the {team.name} team.",
        "success"
    )

    return redirect(
        url_for("team.dashboard")
    )


# =====================================================
# EDIT TEAM
# =====================================================

@admin_bp.route(
    "/teams/<int:team_id>/edit",
    methods=["GET", "POST"]
)
@login_required
@super_admin_required
def edit_team(team_id):

    team = db.session.get(Team, team_id)

    if team is None:
        abort(404)

    form = EditTeamForm(obj=team)

    if form.validate_on_submit():

        team.name = form.name.data
        team.slug = form.slug.data
        team.short_description = form.short_description.data
        team.description = form.description.data
        team.lead_name = form.lead_name.data
        team.lead_role = form.lead_role.data

        db.session.commit()
        print("AFTER COMMIT:", user.activation_token)

        flash(
            "Team updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin.manage_teams")
        )

    return render_template(
        "admin/edit_team.html",
        form=form,
        team=team
    )


# =====================================================
# MANAGE MEMBERS
# =====================================================

@admin_bp.route("/members")
@login_required
@super_admin_required
def manage_members():

    members = MemberProfile.query.order_by(
        MemberProfile.full_name.asc()
    ).all()

    teams = Team.query.order_by(
        Team.name.asc()
    ).all()

    return render_template(
        "admin/members.html",
        members=members,
        teams=teams
    )


@admin_bp.route("/members/add", methods=["GET", "POST"])
@login_required
def add_member():

    form = AddMemberForm()

    teams = Team.query.order_by(
        Team.name.asc()
    ).all()

    form.team_id.choices = [
        (team.id, team.name)
        for team in teams
    ]

    if form.validate_on_submit():

        try:
            # =====================================
            # Prevent duplicate email addresses
            # =====================================
            existing_user = User.query.filter_by(
                email=form.email.data
            ).first()

            if existing_user:
                flash(
                    "A user with this email already exists.",
                    "warning"
                )
                return redirect(
                    url_for("admin.add_member")
                )

            # =====================================
            # Create Public Member Profile
            # =====================================
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

            # =====================================
            # Create Login Account
            # =====================================
            username = generate_username(
                form.full_name.data
            )

            temporary_password = generate_temp_password()

            user = User(
                username=username,
                email=form.email.data,
                role=form.role.data,
                team_id=form.team_id.data,
                is_active=False,
                must_change_password=True,
                activation_token=secrets.token_urlsafe(48)
            )

            print("=" * 60)
            print("NEW USER CREATED")
            print("USERNAME:", user.username)
            print("TOKEN:", user.activation_token)
            print("ACTIVE:", user.is_active)
            print("=" * 60)

            user.set_password(
                temporary_password
            )

            db.session.add(user)

            print("BEFORE COMMIT:", user.activation_token)

            # =====================================
            # Link Profile to User
            # =====================================
            member.user = user

            # =====================================
            # Assign Team Lead
            # =====================================
            if user.role == "team_lead":

                team = Team.query.get(user.team_id)

                if team:
                    team.team_admin = user

            # =====================================
            # Save Records
            # =====================================
            db.session.commit()

            print("AFTER COMMIT:", user.activation_token)

            # =====================================
            # Send Invitation Email
            # =====================================
            try:
                send_member_invitation(
                    user,
                    temporary_password
                )

                flash(
                    "Member account created and invitation email sent.",
                    "success"
                )

            except Exception as email_error:

                current_app.logger.exception(
                    "Invitation email failed"
                )

                print(email_error)

                flash(
                    "Member account was created successfully, but the invitation email could not be sent. The user can be activated later once the email service is working.",
                    "warning"
                )

            return redirect(
                url_for("admin.manage_members")
            )

        except Exception as e:

            db.session.rollback()

            current_app.logger.exception(
                "Member creation failed"
            )

            flash(
                f"Error creating member: {e}",
                "danger"
            )

    return render_template(
        "admin/add_member.html",
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


@admin_bp.route(
    '/members/<int:member_id>/delete',
    methods=['POST']
)
@login_required
def delete_member(member_id):

    member = MemberProfile.query.get_or_404(
        member_id
    )


    # Get connected user account
    user = member.user


    try:

        # Delete user login account first
        if user:

            db.session.delete(user)


        # Delete public profile
        db.session.delete(member)


        db.session.commit()


        flash(
            "Member account deleted permanently.",
            "success"
        )


    except Exception as e:

        db.session.rollback()

        flash(
            f"Delete failed: {e}",
            "danger"
        )


    return redirect(
        url_for(
            'admin.manage_members'
        )
    )
    
@admin_bp.route('/projects')
@login_required
def manage_projects():
    projects = Project.query.order_by(Project.title.asc()).all()

    return render_template(
        'admin/projects.html',
        projects=projects
    )

# =====================================================
# ADD PROJECT
# =====================================================

@admin_bp.route(
    "/projects/add",
    methods=[
        "GET",
        "POST"
    ]
)
@login_required
def add_project():

    teams = Team.query.all()


    if request.method == "POST":

        try:

            # =====================================
            # FORM DATA
            # =====================================

            title = request.form.get(
                "title"
            )

            description = request.form.get(
                "description"
            )

            github_url = request.form.get(
                "github_url"
            )

            demo_url = request.form.get(
                "demo_url"
            )

            visibility = request.form.get(
                "visibility",
                "team"
            )

            team_id = request.form.get(
                "team_id"
            )


            uploaded_file = request.files.get(
                "project_file"
            )


            # =====================================
            # FILE DATA
            # =====================================

            file_url = None
            file_name = None
            file_size = None


            # =====================================
            # CLOUDINARY ZIP UPLOAD
            # =====================================

            if uploaded_file and uploaded_file.filename:


                filename = secure_filename(
                    uploaded_file.filename
                )


                if not filename.lower().endswith(".zip"):

                    flash(
                        "Only ZIP files are allowed.",
                        "danger"
                    )

                    return redirect(
                        url_for(
                            "admin.add_project"
                        )
                    )


                upload_result = upload_project_file(
                    uploaded_file
                )


                file_url = upload_result["url"]

                file_name = filename


                # Calculate size
                uploaded_file.seek(0)

                size = uploaded_file.content_length


                if size:

                    file_size = (
                        f"{round(size / 1024, 2)} KB"
                    )



            # =====================================
            # VISIBILITY CONTROL
            # =====================================

            if visibility == "all_teams":

                team_id = None


            else:

                if not team_id:

                    flash(
                        "Please select a team.",
                        "danger"
                    )

                    return redirect(
                        url_for(
                            "admin.add_project"
                        )
                    )



            # =====================================
            # CREATE PROJECT
            # =====================================

            project = Project(

                title=title,

                description=description,

                github_url=github_url,

                demo_url=demo_url,


                project_file=file_url,

                file_name=file_name,

                file_size=file_size,


                visibility=visibility,

                team_id=team_id,


                created_by=current_user.id

            )


            db.session.add(
                project
            )

            db.session.commit()



            flash(
                "Project uploaded successfully.",
                "success"
            )


            return redirect(
                url_for(
                    "admin.manage_projects"
                )
            )



        except Exception as e:


            db.session.rollback()


            flash(
                f"Project upload failed: {e}",
                "danger"
            )


            return redirect(
                url_for(
                    "admin.add_project"
                )
            )



    return render_template(
        "admin/add_project.html",
        teams=teams
    )
    
@login_required
def edit_project(project_id):


    project = Project.query.get_or_404(
        project_id
    )


    teams = Team.query.all()



    if request.method == "POST":


        project.title = request.form.get(
            "title"
        )


        project.description = request.form.get(
            "description"
        )


        project.github_url = request.form.get(
            "github_url"
        )


        project.demo_url = request.form.get(
            "demo_url"
        )


        project.visibility = request.form.get(
            "visibility"
        )


        team_id = request.form.get(
            "team_id"
        )



        if project.visibility == "all":

            project.team_id = None

        else:

            project.team_id = team_id



        uploaded_file = request.files.get(
            "project_file"
        )



        if uploaded_file and uploaded_file.filename:


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


            save_path = os.path.join(
                upload_folder,
                filename
            )


            uploaded_file.save(
                save_path
            )


            project.project_file = (
                "uploads/projects/"
                + filename
            )


            project.file_name = filename


            size = os.path.getsize(
                save_path
            )


            project.file_size = (
                f"{round(size/1024,2)} KB"
            )



        db.session.commit()



        flash(
            "Project updated successfully.",
            "success"
        )


        return redirect(
            url_for(
                "admin.manage_projects"
            )
        )



    return render_template(
        "admin/edit_project.html",
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


# ---------------------------------------------------------
# View Message
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Mark as Read
# ---------------------------------------------------------
@admin_bp.route("/messages/<int:message_id>/read")
@login_required
def mark_message_read(message_id):

    message = ContactMessage.query.get_or_404(message_id)

    message.is_read = True

    db.session.commit()

    flash("Message marked as read.", "success")

    return redirect(
        url_for("admin.manage_messages")
    )


# ---------------------------------------------------------
# Reply
# ---------------------------------------------------------
@admin_bp.route("/messages/<int:message_id>/reply")
@login_required
def reply_message(message_id):

    message = ContactMessage.query.get_or_404(message_id)

    message.is_read = True
    message.is_replied = True

    db.session.commit()

    from urllib.parse import quote

    subject = quote(f"Re: {message.subject}")

    body = quote(
        f"""Hello {message.full_name},

Thank you for contacting ZeroNexus.

We have received your message and appreciate you reaching out.

Best regards,
ZeroNexus Team
"""
    )

    return redirect(
        f"mailto:{message.email}?subject={subject}&body={body}"
    )


# ---------------------------------------------------------
# Delete Message
# ---------------------------------------------------------
@admin_bp.route(
    "/messages/<int:message_id>/delete",
    methods=["POST"]
)
@login_required
def delete_message(message_id):

    message = ContactMessage.query.get_or_404(message_id)

    db.session.delete(message)

    db.session.commit()

    flash(
        "Message deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.manage_messages")
    )
    
@admin_bp.route(
    "/users/add",
    methods=["GET", "POST"]
)
@login_required
def add_user():

    form = CreateUserForm()


    teams = Team.query.order_by(
        Team.name.asc()
    ).all()


    form.team_id.choices = [
        (
            team.id,
            team.name
        )
        for team in teams
    ]


    if form.validate_on_submit():

        try:

            temporary_password = generate_temp_password()


            username = generate_username(
                form.full_name.data
            )


            user = User(

                username=username,

                email=form.email.data,

                role=form.role.data,

                team_id=form.team_id.data,

                is_active=False,

                activation_token=secrets.token_urlsafe(48)

            )


            user.set_password(
                temporary_password
            )


            db.session.add(user)

            db.session.commit()



            try:

                send_member_invitation(
                    user,
                    temporary_password
                )


                flash(
                    "User created and invitation sent.",
                    "success"
                )


            except Exception as email_error:


                print(
                    f"Email error: {email_error}"
                )


                flash(
                    "User created but email failed.",
                    "warning"
                )


            return redirect(
                url_for(
                    "admin.manage_users"
                )
            )


        except Exception as e:


            db.session.rollback()


            print(
                f"User creation error: {e}"
            )


            flash(
                f"Error creating user: {e}",
                "danger"
            )


    return render_template(
        "admin/add_user.html",
        form=form
    )

@admin_bp.route("/users")
@login_required
def manage_users():

    users = User.query.order_by(
        User.created_at.desc()
    ).all()


    return render_template(
        "admin/users.html",
        users=users
    )

# =====================================================
# MANAGE ANNOUNCEMENTS
# =====================================================

@admin_bp.route("/announcements")
@login_required
@super_admin_required
def manage_announcements():

    announcements = (
        Announcement.query
        .order_by(
            Announcement.pinned.desc(),
            Announcement.created_at.desc()
        )
        .all()
    )

    return render_template(
        "admin/announcements.html",
        announcements=announcements
    )


# =====================================================
# CREATE ANNOUNCEMENT
# =====================================================

@admin_bp.route(
    "/announcements/create",
    methods=["GET", "POST"]
)
@login_required
@super_admin_required
def create_announcement():

    form = CreateAnnouncementForm()

    # Add "All Teams" option
    teams = Team.query.order_by(Team.name.asc()).all()
    
    form = CreateAnnouncementForm(teams=teams)
    

    if form.validate_on_submit():

        # --------------------------------------------------
        # Send announcement to ALL teams
        # --------------------------------------------------
        if form.team_id.data == -1:

            for team in teams:

                announcement = Announcement(
                    title=form.title.data,
                    content=form.content.data,
                    category=form.category.data,
                    pinned=form.pinned.data,
                    team_id=team.id,
                    author_id=current_user.id
                )

                db.session.add(announcement)

            db.session.commit()

            flash(
                "Announcement sent to all teams.",
                "success"
            )

        # --------------------------------------------------
        # Send announcement to one team
        # --------------------------------------------------
        else:

            announcement = Announcement(
                title=form.title.data,
                content=form.content.data,
                category=form.category.data,
                pinned=form.pinned.data,
                team_id=form.team_id.data,
                author_id=current_user.id
            )

            db.session.add(announcement)
            db.session.commit()

            flash(
                "Announcement published.",
                "success"
            )

        return redirect(
            url_for("admin.manage_announcements")
        )

    return render_template(
        "admin/create_announcement.html",
        form=form
    )


# =====================================================
# TOGGLE PIN
# =====================================================

@admin_bp.route(
    "/announcements/<int:announcement_id>/pin",
    methods=["POST"]
)
@login_required
@super_admin_required
def toggle_pin_announcement(announcement_id):

    announcement = db.session.get(Announcement, announcement_id)

    if announcement is None:
        abort(404)

    announcement.pinned = not announcement.pinned
    db.session.commit()

    flash("Announcement updated.", "success")

    return redirect(
        request.referrer or url_for("admin.manage_announcements")
    )


# =====================================================
# DELETE ANNOUNCEMENT
# =====================================================

@admin_bp.route(
    "/announcements/<int:announcement_id>/delete",
    methods=["POST"]
)
@login_required
@super_admin_required
def delete_announcement(announcement_id):

    announcement = db.session.get(Announcement, announcement_id)

    if announcement is None:
        abort(404)

    db.session.delete(announcement)
    db.session.commit()

    flash("Announcement deleted.", "success")

    return redirect(
        url_for("admin.manage_announcements")
    )