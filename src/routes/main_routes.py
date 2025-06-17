# src/routes/main_routes.py
import functools
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from src.models.user import User, db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/services")
def services():
    return render_template("services.html")

@main_bp.route("/services/custom-furniture")
def services_custom_furniture():
    return render_template("services_custom_furniture.html")

@main_bp.route("/services/design-bureau")
def services_design_bureau():
    return render_template("services_design_bureau.html")

@main_bp.route("/services/academy")
def services_academy():
    return render_template("services_academy.html")

@main_bp.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        flash(f"Сообщение от {name} ({email}) на тему \'{subject}\' получено! Мы скоро свяжемся с вами.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

@main_bp.route("/contact/submit", methods=["POST"])
def contact_submit():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        message = request.form.get("message")
        print(f"Получено новое сообщение: Имя: {name}, Email: {email}, Телефон: {phone}, Тема: {subject}, Сообщение: {message}")
        flash("Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.", "success")
        return redirect(url_for("main.contact"))
    return redirect(url_for("main.contact"))

@main_bp.route("/blog")
def blog():
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
    session.pop("username", None)
    session.pop("is_authenticated", None)
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("main.dashboard_login"))

# Decorator to protect dashboard routes
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_authenticated"):
            flash("Пожалуйста, войдите, чтобы получить доступ к этой странице.", "warning")
            return redirect(url_for("main.dashboard_login"))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route("/dashboard")
@main_bp.route("/dashboard/overview")
@login_required
def dashboard_overview():
    return render_template("dashboard.html", dashboard_content_template="dashboard_overview.html")

@main_bp.route("/dashboard/leads")
@login_required
def dashboard_leads():
    leads = [
        {"id": 1, "name": "Иван Петров", "status": "Новый", "score": 0.8, "source": "Форма контактов"},
        {"id": 2, "name": "Анна Сидорова", "status": "В работе", "score": 0.65, "source": "Telegram"},
    ]
    return render_template("dashboard.html", dashboard_content_template="dashboard_leads.html", leads=leads)

@main_bp.route("/dashboard/analytics")
@login_required
def dashboard_analytics():
    return render_template("dashboard.html", dashboard_content_template="dashboard_analytics.html")

@main_bp.route("/dashboard/settings")
@login_required
def dashboard_settings():
    return render_template("dashboard.html", dashboard_content_template="dashboard_settings.html")

