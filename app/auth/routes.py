from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.extensions import db

from app.models import User

from . import auth_bp

from .forms import (
    LoginForm,
    ActivateAccountForm
)


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:

        if current_user.role == "admin":

            return redirect(
                url_for("admin.dashboard")
            )

        elif current_user.role == "team_lead":

            return redirect(
                url_for("team.dashboard")
            )

        else:

            return redirect(
                url_for("user.profile")
            )

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter(
            (
                User.username == form.username.data
            )
            |
            (
                User.email == form.username.data
            )
        ).first()

        if not user:

            flash(
                "Invalid username or password.",
                "danger"
            )

            return redirect(
                url_for("main.index")
            )

        if not user.is_active:

            flash(
                "Please activate your account first.",
                "warning"
            )

            return redirect(
                url_for(
                    "auth.activate_account",
                    token=user.activation_token
                )
            )

        if not user.check_password(
            form.password.data
        ):

            flash(
                "Invalid username or password.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(user)

        if user.must_change_password:

            return redirect(
                url_for(
                    "auth.activate_account",
                    token=user.activation_token
                )
            )

        # -----------------------------------------
        # Redirect according to role
        # -----------------------------------------

        if user.role == "admin":

            return redirect(
                url_for("admin.dashboard")
            )

        elif user.role == "team_lead":

            return redirect(
                url_for("team.dashboard")
            )

        else:

            return redirect(
                url_for("user.profile")
            )

    return render_template(
        "auth/login.html",
        form=form
    )


# =====================================================
# ACCOUNT ACTIVATION
# =====================================================

@auth_bp.route(
    "/activate/<token>",
    methods=["GET", "POST"]
)
def activate_account(token):

    user = User.query.filter_by(
        activation_token=token
    ).first_or_404()

    if user.is_active:

        flash(
            "Account already activated.",
            "info"
        )

        return redirect(
            url_for("auth.login")
        )

    form = ActivateAccountForm()

    if form.validate_on_submit():

        try:

            print("========== ACTIVATION START ==========")
            print("STEP 1")

            user.set_password(
                form.password.data
            )

            print("STEP 2")

            user.is_active = True
            user.must_change_password = False
            user.activation_token = None

            print("STEP 3")

            db.session.commit()

            print("STEP 4 - DATABASE COMMIT SUCCESS")

            login_user(user)

            print("STEP 5 - LOGIN SUCCESS")
            print("ROLE =", user.role)

        except Exception:

            db.session.rollback()

            import traceback
            traceback.print_exc()

            raise

        flash(
            "Account activated successfully.",
            "success"
        )

        # -----------------------------------------
        # Redirect according to role
        # -----------------------------------------

        if user.role == "admin":

            return redirect(
                url_for("admin.dashboard")
            )

        elif user.role == "team_lead":

            return redirect(
                url_for("team.dashboard")
            )

        else:

            return redirect(
                url_for("user.profile")
            )

    return render_template(
        "auth/activate_account.html",
        form=form,
        user=user
    )

# =====================================================
# TEAM DASHBOARD
# =====================================================

@auth_bp.route("/dashboard")
@login_required
def dashboard():


    return render_template(
        "auth/dashboard.html",
        user=current_user
    )



# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()


    flash(
        "Logged out successfully.",
        "success"
    )


    return redirect(
        url_for("main.index")
    )