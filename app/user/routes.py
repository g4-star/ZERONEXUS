from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import User

from . import user_bp


# =====================================
# Account Activation
# =====================================

@user_bp.route(
    "/activate/<token>",
    methods=["GET", "POST"]
)
def activate_account(token):

    user = User.query.filter_by(
        activation_token=token
    ).first_or_404()


    if user.is_active:

        flash(
            "Account already activated. Please login.",
            "info"
        )

        return redirect(
            url_for("user.login")
        )


    if request.method == "POST":

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                request.url
            )


        user.password_hash = generate_password_hash(
            password
        )


        user.must_change_password = False

        user.is_active = True


        db.session.commit()


        flash(
            "Account activated successfully. You can now login.",
            "success"
        )


        return redirect(
            url_for("user.login")
        )


    return render_template(
        "user/activate.html",
        user=user
    )
