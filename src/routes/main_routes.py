
"""Main routes for BaiMuras application."""

import functools
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
from src.models.user import User, db
from src.utils import get_current_language
from src.utils.consultation_helper import create_consultation_request, get_consultation_error_response
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
    if language in ['ru', 'ky']:
        session['language'] = language
        flash("Language updated successfully", "success")
    return redirect(request.referrer or url_for('main.index'))


@main_bp.route("/about")
def about():
    """About page."""
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
    """Kitchens service page."""
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


@main_bp.route("/blog")
def blog():
    """Blog page."""
    return render_template("blog.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact page with consultation form."""
    current_lang = get_current_language()
    form_content = CONTACT_FORM.get(current_lang, CONTACT_FORM['ru'])

    if request.method == "POST":
        try:
            # Validate required fields
            required_fields = ['name', 'phone', 'service_type', 'message']
            form_data = request.form.to_dict()
            
            for field in required_fields:
                if not form_data.get(field, '').strip():
                    flash(f"Поле '{field}' обязательно для заполнения", "error")
                    return render_template("contact.html", form_content=form_content)
            
            # Create consultation request
            create_consultation_request(form_data)
            flash(form_content['success_message'], "success")
            return redirect(url_for("main.contact"))

        except ValueError as validation_error:
            flash(str(validation_error), "error")
            return render_template("contact.html", form_content=form_content)
        except (RuntimeError, OSError, IOError) as consultation_error:
            db.session.rollback()
            flash(form_content['error_message'], "error")
            print(f"Error saving consultation request: {consultation_error}")

    return render_template("contact.html", form_content=form_content)


@main_bp.route("/api/consultation", methods=["POST"])
def api_consultation():
    """API endpoint for consultation requests."""
    try:
        data = request.get_json()
        consultation = create_consultation_request(data)

        return jsonify({
            "success": True,
            "message": "Consultation request submitted successfully",
            "data": consultation.to_dict()
        }), 200

    except ValueError as validation_error:
        return jsonify(get_consultation_error_response(str(validation_error))), 400
    except (RuntimeError, OSError, IOError):
        db.session.rollback()
        return jsonify(get_consultation_error_response()), 500


@main_bp.route("/services/custom-furniture")
def services_custom_furniture():
    """Custom furniture service page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services_custom_furniture.html", service=content.get('custom_furniture', content['montessori']))


@main_bp.route("/services/design-bureau")
def services_design_bureau():
    """Design bureau service page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services_design_bureau.html", service=content.get('design_bureau', content['kitchens']))


@main_bp.route("/services/academy")
def services_academy():
    """Academy service page."""
    current_lang = get_current_language()
    content = SERVICES.get(current_lang, SERVICES['ru'])
    return render_template("services_academy.html", service=content.get('academy', content['montessori']))


@main_bp.route("/dashboard")
def dashboard():
    """Dashboard overview."""
    return render_template("dashboard_overview.html")


@main_bp.route("/dashboard/analytics")
def dashboard_analytics():
    """Dashboard analytics page."""
    return render_template("dashboard_analytics.html")


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration."""
    if request.method == "POST":
        try:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            # Check if user already exists
            if User.query.filter_by(username=username).first():
                flash("Username already exists", "error")
                return render_template("register.html")

            if User.query.filter_by(email=email).first():
                flash("Email already registered", "error")
                return render_template("register.html")

            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Registration successful", "success")
            return redirect(url_for("main.index"))

        except (ValueError, RuntimeError, OSError) as register_error:
            db.session.rollback()
            flash("Registration failed", "error")
            print(f"Registration error: {register_error}")

    return render_template("register.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash("Login successful", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid credentials", "error")

    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    """User logout."""
    session.pop('user_id', None)
    flash("Logged out successfully", "success")
    return redirect(url_for("main.index"))


def login_required(func):
    """Decorator for login required routes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)
    return wrapper
