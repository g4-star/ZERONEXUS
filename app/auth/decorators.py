from functools import wraps

from flask import (
    abort,
    flash,
    redirect,
    url_for
)

from flask_login import (
    current_user
)


# =====================================
# Super Admin Permission
# =====================================

def super_admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:

            return redirect(
                url_for("auth.login")
            )

        if current_user.role != "super_admin":

            flash(
                "You do not have permission to access this page.",
                "danger"
            )

            abort(403)

        return function(
            *args,
            **kwargs
        )

    return wrapper


# =====================================
# Team Lead Permission
# =====================================

def team_lead_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:

            return redirect(
                url_for("auth.login")
            )

        if current_user.role not in [
            "super_admin",
            "team_lead"
        ]:

            flash(
                "You do not have permission to access this page.",
                "danger"
            )

            abort(403)

        return function(
            *args,
            **kwargs
        )

    return wrapper


# =====================================
# Member Permission
# =====================================

def member_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:

            return redirect(
                url_for("auth.login")
            )

        if current_user.role not in [
            "super_admin",
            "team_lead",
            "member"
        ]:

            flash(
                "Access denied.",
                "danger"
            )

            abort(403)

        return function(
            *args,
            **kwargs
        )

    return wrapper