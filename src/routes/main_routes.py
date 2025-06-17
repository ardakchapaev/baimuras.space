"""Module docstring."""

import functools

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from src.models.user import User, db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Function docstring."""
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Function docstring."""
    return render_template("about.html")


@main_bp.route("/services")
def services():
    """Function docstring."""
    return render_template("services.html")


@main_bp.route("/services/custom-furniture")
def services_custom_furniture():
    """Function docstring."""
    return render_template("services_custom_furniture.html")


@main_bp.route("/services/design-bureau")
def services_design_bureau():
    """Function docstring."""
    return render_template("services_design_bureau.html")


@main_bp.route("/services/academy")
def services_academy():
    """Function docstring."""
    return render_template("services_academy.html")


@main_bp.route("/portfolio")
def portfolio():
    """Function docstring."""
    return render_template("portfolio.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Function docstring."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        request.form.get("message")
        flash(
            f"Сообщение от {name} ({email}) на тему '{subject}' получено! Мы скоро свяжемся с вами.",
            "success",
        )
        return redirect(url_for("main.contact"))
    return render_template("contact.html")


@main_bp.route("/contact/submit", methods=["POST"])
def contact_submit():
    """Function docstring."""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        message = request.form.get("message")
        print(
            f"Получено новое сообщение: Имя: {name}, Email: {email}, Телефон: {phone}, Тема: {subject}, Сообщение: {message}"
        )
        flash(
            "Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.",
            "success",
        )
        return redirect(url_for("main.contact"))
    return redirect(url_for("main.contact"))


@main_bp.route("/blog")
def blog():
    """Function docstring."""
    return render_template("blog.html")


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            flash("Имя пользователя уже занято.", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна. Теперь войдите в систему.", "success")
            return redirect(url_for("main.dashboard_login"))
    return render_template("register.html")


@main_bp.route("/dashboard/login", methods=["GET", "POST"])
def dashboard_login():
    """Function docstring."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["username"] = username
            session["is_authenticated"] = True
            flash("Вход выполнен успешно!", "success")
            return redirect(url_for("main.dashboard_overview"))
        else:
            flash("Неверное имя пользователя или пароль.", "danger")
    return render_template("dashboard_login.html")


@main_bp.route("/dashboard/logout")
def dashboard_logout():
    """Function docstring."""
    session.pop("username", None)
    session.pop("is_authenticated", None)
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("main.dashboard_login"))


# Декоратор для защиты маршрутов дашборда
def login_required(f):
    """Function docstring."""

    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        """Function docstring."""
        if not session.get("is_authenticated"):
            flash(
                "Пожалуйста, войдите, чтобы получить доступ к этой странице.", "warning"
            )
            return redirect(url_for("main.dashboard_login"))
        return f(*args, **kwargs)

    return decorated_function


@main_bp.route("/dashboard")
@main_bp.route("/dashboard/overview")
@login_required
def dashboard_overview():
    """Function docstring."""
    return render_template(
        "dashboard.html", dashboard_content_template="dashboard_overview.html"
    )


@main_bp.route("/dashboard/leads")
@login_required
def dashboard_leads():
    """Function docstring."""
    from src.models.lead import Lead

    leads = Lead.query.all()
    return render_template(
        "dashboard.html", dashboard_content_template="dashboard_leads.html", leads=leads
    )


@main_bp.route("/dashboard/analytics")
@login_required
def dashboard_analytics():
    """Function docstring."""
    return render_template(
        "dashboard.html", dashboard_content_template="dashboard_analytics.html"
    )


@main_bp.route("/dashboard/settings")
@login_required
def dashboard_settings():
    """Function docstring."""
    return render_template(
        "dashboard.html", dashboard_content_template="dashboard_settings.html"
    )
