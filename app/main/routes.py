from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    session
)

from app.models import (
    Team,
    MemberProfile,
    ContactMessage
)

from app.main.forms import (
    MemberProfileForm,
    ContactForm
)
from app.extensions import db
import cloudinary.uploader
from app.email import (
    send_member_welcome,
    send_contact_confirmation
)


main_bp = Blueprint('main', __name__)


# -------------------------------------------------
# Home Page
# -------------------------------------------------
@main_bp.route("/", methods=["GET", "POST"])
def index():

    # -----------------------------------------
    # Load Contact Form
    # -----------------------------------------
    form = ContactForm()

    # -----------------------------------------
    # Load Teams
    # -----------------------------------------
    teams = Team.query.order_by(
        Team.name.asc()
    ).all()

    # -----------------------------------------
    # Handle Contact Form Submission
    # -----------------------------------------
    if form.validate_on_submit():

        try:

            new_message = ContactMessage(
                full_name=form.full_name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )

            db.session.add(new_message)
            db.session.commit()

            # Send confirmation email
            try:
                send_contact_confirmation(new_message)
            except Exception as e:
                print(f"Confirmation email failed: {e}")

            flash(
                "🎉 Thank you for contacting ZeroNexus! Your message has been submitted successfully. We truly appreciate your feedback and will get back to you as soon as possible.",
                "success"
            )

            return redirect(
                url_for("main.index") + "#contact"
            )

        except Exception as e:

            db.session.rollback()

            flash(
                f"An error occurred: {str(e)}",
                "danger"
            )

    return render_template(
        "main/index.html",
        teams=teams,
        form=form
    )


# -------------------------------------------------
# Teams Page
# -------------------------------------------------
@main_bp.route('/teams')
def teams():
    teams = Team.query.order_by(Team.name.asc()).all()
    return render_template('main/teams.html', teams=teams)


# -------------------------------------------------
# Team Detail Page
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
@main_bp.route("/member/edit/<token>", methods=["GET", "POST"])
def edit_member(token):
    from flask import flash, redirect, render_template, url_for, session
    import cloudinary.uploader

    member = MemberProfile.query.filter_by(
        profile_token=token
    ).first_or_404()

    form = MemberProfileForm(obj=member)

    if form.validate_on_submit():

        # -----------------------------------------
        # Upload profile picture to Cloudinary
        # -----------------------------------------
        if form.photo.data:
            try:
                upload_result = cloudinary.uploader.upload(
                    form.photo.data,
                    folder="zeronexus/members"
                )

                print("========== CLOUDINARY RESULT ==========")
                print(upload_result)
                print("=======================================")

                member.photo = upload_result.get("secure_url")

            except Exception as e:
                print("========== CLOUDINARY ERROR ==========")
                print(str(e))
                print("======================================")

                flash(
                    f"Image upload failed: {str(e)}",
                    "danger"
                )

                return render_template(
                    "main/edit_member.html",
                    form=form,
                    member=member
                )

        # -----------------------------------------
        # Update member information
        # -----------------------------------------
        member.full_name = form.full_name.data
        member.role = form.role.data
        member.bio = form.bio.data
        member.linkedin_url = form.linkedin_url.data
        member.github_url = form.github_url.data
        member.portfolio_url = form.portfolio_url.data
        member.email = form.email.data
        member.whatsapp_number = form.whatsapp_number.data
        member.skills = form.skills.data

        # -----------------------------------------
        # Save changes
        # -----------------------------------------
        try:
            db.session.commit()

            session.pop("_flashes", None)

            flash(
                "Your profile has been updated successfully.",
                "success"
            )

            return redirect(url_for("main.index"))

        except Exception as e:
            db.session.rollback()

            print("========== DATABASE ERROR ==========")
            print(str(e))
            print("====================================")

            flash(
                f"Database error: {str(e)}",
                "danger"
            )

    else:
        if form.errors:
            print("========== FORM ERRORS ==========")
            print(form.errors)
            print("=================================")

    return render_template(
        "main/edit_member.html",
        form=form,
        member=member
    )
    
