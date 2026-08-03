from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.extensions import db

from . import user_bp
from .forms import EditProfileForm
from app.cloudinary_config import upload_image
from app.models.project import Project
from app.models.announcement import Announcement
from app.models.meeting import Meeting


# =====================================================
# PROFILE
# =====================================================

@user_bp.route("/profile")
@login_required
def profile():
    return redirect(url_for("team.profile"))

# =====================================================
# EDIT PROFILE
# =====================================================

@user_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():

    form = EditProfileForm()

    # ----------------------------------------
    # Populate existing values
    # ----------------------------------------

    if request.method == "GET":
        form.full_name.data = current_user.full_name
        form.username.data = current_user.username
        form.bio.data = current_user.bio
        form.phone.data = current_user.phone
        form.whatsapp.data = current_user.whatsapp
        form.location.data = current_user.location

        form.skills.data = current_user.skills
        form.job_title.data = current_user.job_title
        form.company.data = current_user.company
        form.experience_level.data = current_user.experience_level
        form.favorite_language.data = current_user.favorite_language

        form.portfolio.data = current_user.portfolio
        form.github.data = current_user.github
        form.linkedin.data = current_user.linkedin
        form.twitter.data = current_user.twitter

        form.tryhackme.data = current_user.tryhackme
        form.hackthebox.data = current_user.hackthebox
        form.ctftime.data = current_user.ctftime

    # ----------------------------------------
    # Save profile
    # ----------------------------------------

    if form.validate_on_submit():

        current_user.full_name = form.full_name.data
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.phone = form.phone.data
        current_user.whatsapp = form.whatsapp.data
        current_user.location = form.location.data

        current_user.skills = form.skills.data
        current_user.job_title = form.job_title.data
        current_user.company = form.company.data
        current_user.experience_level = form.experience_level.data
        current_user.favorite_language = form.favorite_language.data

        current_user.portfolio = form.portfolio.data
        current_user.github = form.github.data
        current_user.linkedin = form.linkedin.data
        current_user.twitter = form.twitter.data

        current_user.tryhackme = form.tryhackme.data
        current_user.hackthebox = form.hackthebox.data
        current_user.ctftime = form.ctftime.data

        if form.profile_image.data:
            image_url = upload_image(form.profile_image.data)
            current_user.profile_image = image_url

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("user.profile"))

    return render_template(
        "user/edit_profile.html",
        form=form,
        user=current_user
    )