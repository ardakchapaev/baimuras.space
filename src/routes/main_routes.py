
"""Main routes for BaiMuras application."""

import functools
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
from src.models.user import User, db
from src.models.consultation import ConsultationRequest
from src.utils import get_current_language, set_language, get_localized_content
from src.content import HOMEPAGE, SERVICES, CONTACT_FORM

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Homepage."""
    current_lang = get_current_language()
    content = HOMEPAGE.get(current_lang, HOMEPAGE['ru'])
    return render_template("index.html", content=content)


@main_bp.route("/set-language/<language>")
def set_language_route(language):
    """Set language preference."""
    if set_language(language):
        flash("Language updated successfully", "success")
    return redirect(request.referrer or url_for('main.index'))


@main_bp.route("/about")
def about():
    """About page."""
    current_lang = get_current_language()
    return render_template("about.html")


@main_bp.route("/services")
def services():
    """Services overview page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services.html", services_content=content)


@main_bp.route("/services/montessori")
def services_montessori():
    """Montessori furniture service page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services_montessori.html", service=content['montessori'])


@main_bp.route("/services/kitchens")
def services_kitchens():
    """Custom kitchens service page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services_kitchens.html", service=content['kitchens'])


@main_bp.route("/services/children-rooms")
def services_children_rooms():
    """Children rooms service page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services_children_rooms.html", service=content['children_rooms'])


@main_bp.route("/portfolio")
def portfolio():
    """Portfolio page."""
    return render_template("portfolio.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page with consultation form."""
    current_lang = get_current_language()
    form_content = CONTACT_FORM.get(current_lang, CONTACT_FORM['ru'])
    
    if request.method == "POST":
        try:
            # Create consultation request
            consultation = ConsultationRequest(
                name=request.form.get("name"),
                phone=request.form.get("phone"),
                email=request.form.get("email"),
                service_type=request.form.get("service_type"),
                message=request.form.get("message"),
                language=current_lang
            )
            
            db.session.add(consultation)
            db.session.commit()
            
            flash(form_content['success_message'], "success")
            return redirect(url_for("main.contact"))
            
        except Exception as e:
            db.session.rollback()
            flash(form_content['error_message'], "error")
            print(f"Error saving consultation request: {e}")
    
    return render_template("contact.html", form_content=form_content)


@main_bp.route("/api/consultation", methods=["POST"])
def api_consultation():
    """API endpoint for consultation requests."""
    try:
        data = request.get_json()
        
        consultation = ConsultationRequest(
            name=data.get("name"),
            phone=data.get("phone"),
            email=data.get("email"),
            service_type=data.get("service_type"),
            message=data.get("message"),
            language=data.get("language", "ru")
        )
        
        db.session.add(consultation)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Consultation request submitted successfully",
            "id": consultation.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Error submitting consultation request"
        }), 500


# Legacy routes for backward compatibility
@main_bp.route("/services/custom-furniture")
def services_custom_furniture():
    """Legacy route redirect."""
    return redirect(url_for('main.services_montessori'))


@main_bp.route("/services/design-bureau")
def services_design_bureau():
    """Legacy route redirect."""
    return redirect(url_for('main.services_kitchens'))


@main_bp.route("/services/academy")
def services_academy():
    """Legacy route redirect."""
    return redirect(url_for('main.services'))


@main_bp.route("/blog")
def blog():
    """Blog page (placeholder)."""
    return render_template("blog.html")


# Dashboard routes (keeping existing functionality)
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
    """Dashboard login."""
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
    """Dashboard logout."""
    session.pop("username", None)
    session.pop("is_authenticated", None)
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("main.dashboard_login"))


# Декоратор для защиты маршрутов дашборда
def login_required(f):
    """Login required decorator."""
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
    """Dashboard overview."""
    return render_template("dashboard.html", dashboard_content_template="dashboard_overview.html")


@main_bp.route("/dashboard/leads")
@login_required
def dashboard_leads():
    """Dashboard leads management."""
    consultations = ConsultationRequest.query.order_by(ConsultationRequest.created_at.desc()).all()
    return render_template("dashboard.html", 
                         dashboard_content_template="dashboard_leads.html", 
                         consultations=consultations)


@main_bp.route("/dashboard/analytics")
@login_required
def dashboard_analytics():
    """Dashboard analytics."""
    return render_template("dashboard.html", dashboard_content_template="dashboard_analytics.html")


@main_bp.route("/dashboard/settings")
@login_required
def dashboard_settings():
    """Dashboard settings."""
    return render_template("dashboard.html", dashboard_content_template="dashboard_settings.html")
