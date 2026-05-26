from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.db import get_db  # safe DB connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        connection = get_db()
        if not connection:
            flash("Database connection error", "danger")
            return render_template("auth/login.html")

        try:
            with connection.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cur.fetchone()

            if user and check_password_hash(user["password_hash"], password):
                user_obj = User(
                    user["id"], user["username"], user["password"], user["role"]
                )
                login_user(user_obj)
                next_page = request.args.get("next")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for("dashboard.dashboard"))
                )
            else:
                flash("Invalid username or password", "danger")

        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if len(username) < 4 or len(username) > 20:
            flash("Username must be between 4-20 characters", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters", "danger")
            return render_template("auth/register.html")

        connection = get_db()
        if not connection:
            flash("Database connection error", "danger")
            return render_template("auth/register.html")

        try:
            with connection.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE username = %s", (username,))
                if cur.fetchone():
                    flash("Username already exists", "danger")
                    return render_template("auth/register.html")

                password_hash = generate_password_hash(password)
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                    (username, password_hash),
                )
                connection.commit()

                flash("Registration successful! Please login.", "success")
                return redirect(url_for("auth.login"))

        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")

    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("auth/profile.html", user=current_user)


@auth_bp.route("/settings")
@login_required
def settings():
    return render_template("settings/settings.html", user=current_user)


@auth_bp.route("/update-profile", methods=["POST"])
@login_required
def update_profile():
    full_name = request.form.get("full_name")
    phone = request.form.get("phone")

    connection = get_db()
    if not connection:
        flash("Database connection error", "danger")
        return redirect(url_for("auth.settings"))

    try:
        with connection.cursor() as cur:
            cur.execute(
                "UPDATE users SET username=%s, phone=%s WHERE id=%s",
                (full_name, phone, current_user.id),
            )
            connection.commit()
        flash("Profile updated successfully!", "success")
    except Exception as e:
        flash(f"Database error: {str(e)}", "danger")

    return redirect(url_for("auth.settings"))


@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    current_pw = request.form.get("current_password")
    new_pw = request.form.get("new_password")
    confirm_pw = request.form.get("confirm_password")

    connection = get_db()
    if not connection:
        flash("Database connection error", "danger")
        return redirect(url_for("auth.settings"))

    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT password_hash FROM users WHERE id=%s", (current_user.id,)
            )
            user = cur.fetchone()

            if not check_password_hash(user["password_hash"], current_pw):
                flash("Current password is incorrect!", "danger")
                return redirect(url_for("auth.settings"))

            if new_pw != confirm_pw:
                flash("New passwords do not match!", "danger")
                return redirect(url_for("auth.settings"))

            new_hash = generate_password_hash(new_pw)
            cur.execute(
                "UPDATE users SET password_hash=%s WHERE id=%s",
                (new_hash, current_user.id),
            )
            connection.commit()

            flash("Password changed successfully!", "success")

    except Exception as e:
        flash(f"Database error: {str(e)}", "danger")

    return redirect(url_for("auth.settings"))
