"""CRM routes for managing leads and projects."""

from flask import Blueprint, render_template, redirect, url_for

from src.routes.main_routes import login_required
from src.models import Lead, Project

crm_bp = Blueprint('crm', __name__, url_prefix='/crm')

@crm_bp.route('/leads')
@login_required
def crm_leads():
    """Display all leads."""
    leads = Lead.query.all()
    return render_template('dashboard_leads.html', leads=leads)

@crm_bp.route('/projects')
@login_required
def crm_projects():
    """Display all projects."""
    projects = Project.query.all()
    return render_template('dashboard_projects.html', projects=projects)

