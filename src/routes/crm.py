"""CRM routes for managing leads and projects."""

from flask import Blueprint, render_template

from src.models import Lead, Project
from src.utils.auth import login_required

crm_bp = Blueprint("crm", __name__, url_prefix="/crm")


@crm_bp.route("/leads")
@login_required
def crm_leads():
    """Display all leads."""
    leads = Lead.query.all()
    return render_template("dashboard_leads.html", leads=leads)


@crm_bp.route("/projects")
@login_required
def crm_projects():
    """Display all projects."""
    projects = Project.query.all()
    return render_template("dashboard_projects.html", projects=projects)
