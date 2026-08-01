from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user
)

from app.auth import auth_bp
from app.models import User


@auth_bp.route(
    "/login",
    methods=["GET","POST"]
)
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )


    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        password = request.form.get(
            "password"
        )


        user = User.query.filter_by(
            username=username
        ).first()


        if user and user.check_password(password):

            login_user(user)


            if user.must_change_password:

                return redirect(
                    url_for(
                        "auth.change_password"
                    )
                )


            return redirect(
                url_for(
                    "main.dashboard"
                )
            )


        flash(
            "Invalid username or password.",
            "danger"
        )


    return render_template(
        "auth/login.html"
    )



@auth_bp.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("main.index")
    )



@auth_bp.route(
    "/change-password",
    methods=["GET","POST"]
)
def change_password():

    if request.method=="POST":

        password=request.form.get(
            "password"
        )


        current_user.set_password(
            password
        )


        current_user.must_change_password=False


        from app.extensions import db

        db.session.commit()


        flash(
            "Password updated successfully.",
            "success"
        )


        return redirect(
            url_for(
                "main.dashboard"
            )
        )


    return render_template(
        "auth/change_password.html"
    )