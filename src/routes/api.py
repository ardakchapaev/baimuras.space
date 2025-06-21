
"""API routes for BaiMuras application."""

from flask import Blueprint, request, jsonify
from src.models.consultation import ConsultationRequest, db
from src.models.user import User
from src.models.project import Project
from src.models.lead import Lead
from src.utils.consultation_helper import (
    create_consultation_request,
    get_consultation_success_response,
    get_consultation_error_response
)
from src.utils import send_event

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "message": "API is running"}), 200


@api_bp.route("/consultations", methods=["GET"])
def get_consultations():
    """Get all consultation requests."""
    try:
        consultations = ConsultationRequest.query.all()
        return jsonify({
            "success": True,
            "data": [consultation.to_dict() for consultation in consultations]
        }), 200
    except Exception:
        return jsonify(get_consultation_error_response(
            "Error fetching consultations")), 500


@api_bp.route("/consultations", methods=["POST"])
def create_consultation():
    """Create new consultation request."""
    try:
        data = request.get_json()
        consultation = create_consultation_request(data)
        send_event('consultation.created', consultation.to_dict())
        return jsonify(get_consultation_success_response(consultation)), 201

    except ValueError as validation_error:
        return jsonify(
            get_consultation_error_response(
                str(validation_error))), 400
    except Exception:
        db.session.rollback()
        return jsonify(get_consultation_error_response()), 500


@api_bp.route("/consultations/<int:consultation_id>", methods=["GET"])
def get_consultation(consultation_id):
    """Get specific consultation request."""
    try:
        consultation = ConsultationRequest.query.get_or_404(consultation_id)
        return jsonify({
            "success": True,
            "data": consultation.to_dict()
        }), 200
    except Exception:
        return jsonify(get_consultation_error_response(
            "Consultation not found")), 404


@api_bp.route("/consultations/<int:consultation_id>", methods=["PUT"])
def update_consultation(consultation_id):
    """Update consultation request status."""
    try:
        consultation = ConsultationRequest.query.get_or_404(consultation_id)
        data = request.get_json()

        if "status" in data:
            consultation.status = data["status"]

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Consultation updated successfully",
            "data": consultation.to_dict()
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify(get_consultation_error_response(
            "Error updating consultation")), 500


@api_bp.route("/users", methods=["GET"])
def get_users():
    """Get all users."""
    try:
        users = User.query.all()
        return jsonify({
            "success": True,
            "data": [user.to_dict() for user in users]
        }), 200
    except Exception:
        return jsonify(get_consultation_error_response(
            "Error fetching users")), 500


@api_bp.route("/projects", methods=["GET"])
def get_projects():
    """Get all projects."""
    try:
        projects = Project.query.all()
        return jsonify({
            "success": True,
            "data": [project.to_dict() for project in projects]
        }), 200
    except Exception:
        return jsonify(get_consultation_error_response(
            "Error fetching projects")), 500


@api_bp.route("/leads", methods=["GET"])
def get_leads():
    """Get all leads."""
    try:
        leads = Lead.query.all()
        return jsonify({
            "success": True,
            "data": [lead.to_dict() for lead in leads]
        }), 200
    except Exception:
        return jsonify(get_consultation_error_response(
            "Error fetching leads")), 500


@api_bp.route("/leads", methods=["POST"])
def create_lead():
    """Create new lead."""
    try:
        data = request.get_json()

        if not data.get("name") or not data.get("contact"):
            return jsonify(get_consultation_error_response(
                "Name and contact are required")), 400

        lead = Lead(
            name=data.get("name"),
            contact=data.get("contact"),
            source=data.get("source", "website"),
            status=data.get("status", "new")
        )

        db.session.add(lead)
        db.session.commit()
        send_event('lead.created', lead.to_dict())

        return jsonify({
            "success": True,
            "message": "Lead created successfully",
            "data": lead.to_dict()
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify(get_consultation_error_response(
            "Error creating lead")), 500


@api_bp.route("/webhooks", methods=["POST"])
def trigger_webhook():
    """Endpoint to receive webhook events and forward to n8n."""
    data = request.get_json() or {}
    event = data.get("event", "unknown")
    send_event(event, data.get("payload", {}))
    return jsonify({"success": True}), 201
