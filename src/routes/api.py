"""Module docstring."""

import os
from functools import wraps

from flask import Blueprint, jsonify, request

from src.models.lead import Lead
from src.models.project import Project
from src.models.user import db

api_bp = Blueprint("api", __name__)


def require_api_key(f):
    """Function docstring."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """Function docstring."""
        api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
        expected_key = os.environ.get("API_KEY", "dev-api-key-change-in-production")

        if not api_key or api_key != expected_key:
            return jsonify({"error": "Invalid or missing API key"}), 401

        return f(*args, **kwargs)

    return decorated_function


@api_bp.route("/webhooks/contact", methods=["POST"])
def webhook_contact():
    """Webhook для получения контактных форм от n8n"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Создаем новый лид из контактной формы
        lead = Lead(
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            subject=data.get("subject", ""),
            message=data.get("message", ""),
            source=data.get("source", "website"),
            score=0.5,  # Базовый скор для контактных форм
        )

        db.session.add(lead)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "lead_id": lead.id,
                    "message": "Contact form processed successfully",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api_bp.route("/webhooks/lead", methods=["POST"])
@require_api_key
def webhook_lead():
    """Webhook для создания/обновления лидов от n8n"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        lead_id = data.get("lead_id")

        if lead_id:
            # Обновляем существующий лид
            lead = Lead.query.get(lead_id)
            if not lead:
                return jsonify({"error": "Lead not found"}), 404

            # Обновляем поля
            for field in [
                "name",
                "email",
                "phone",
                "subject",
                "message",
                "status",
                "score",
                "source",
            ]:
                if field in data:
                    setattr(lead, field, data[field])
        else:
            # Создаем новый лид
            lead = Lead(
                name=data.get("name", ""),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                subject=data.get("subject", ""),
                message=data.get("message", ""),
                status=data.get("status", "new"),
                score=data.get("score", 0.0),
                source=data.get("source", "api"),
            )
            db.session.add(lead)

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "lead_id": lead.id,
                "message": "Lead processed successfully",
            }
        ), (201 if not lead_id else 200)

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api_bp.route("/leads", methods=["GET"])
@require_api_key
def get_leads():
    """Получить список всех лидов"""
    try:
        leads = Lead.query.all()
        return jsonify({"success": True, "leads": [lead.to_dict() for lead in leads]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/leads/<int:lead_id>", methods=["GET"])
@require_api_key
def get_lead(lead_id):
    """Получить конкретный лид"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        return jsonify({"success": True, "lead": lead.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/leads/<int:lead_id>", methods=["PUT"])
@require_api_key
def update_lead(lead_id):
    """Обновить лид"""
    try:
        lead = Lead.query.get_or_404(lead_id)
        data = request.get_json()

        for field in [
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "status",
            "score",
            "source",
        ]:
            if field in data:
                setattr(lead, field, data[field])

        db.session.commit()

        return jsonify({"success": True, "lead": lead.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api_bp.route("/projects", methods=["GET"])
@require_api_key
def get_projects():
    """Получить список всех проектов"""
    try:
        projects = Project.query.all()
        return jsonify(
            {"success": True, "projects": [project.to_dict() for project in projects]}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/projects", methods=["POST"])
@require_api_key
def create_project():
    """Создать новый проект"""
    try:
        data = request.get_json()

        if not data or not data.get("title"):
            return jsonify({"error": "Title is required"}), 400

        project = Project(
            title=data.get("title"),
            description=data.get("description", ""),
            project_type=data.get("project_type", ""),
            status=data.get("status", "planning"),
            budget=data.get("budget"),
            lead_id=data.get("lead_id"),
        )

        db.session.add(project)
        db.session.commit()

        return jsonify({"success": True, "project": project.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api_bp.route("/health", methods=["GET"])
def api_health():
    """API health check"""
    return jsonify(
        {
            "status": "healthy",
            "version": "1.0.0",
            "endpoints": [
                "/api/webhooks/contact",
                "/api/webhooks/lead",
                "/api/leads",
                "/api/projects",
            ],
        }
    )
