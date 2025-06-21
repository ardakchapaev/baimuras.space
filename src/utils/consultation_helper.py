"""Helper functions for consultation request handling."""

from src.models.consultation import ConsultationRequest, db


def create_consultation_request(data):
    """Create a new consultation request.

    Args:
        data: Dictionary containing consultation data

    Returns:
        ConsultationRequest: Created consultation instance

    Raises:
        ValueError: If required fields are missing
    """
    if not data.get("name") or not data.get("phone"):
        raise ValueError("Name and phone are required")

    consultation = ConsultationRequest(
        name=data.get("name"),
        phone=data.get("phone"),
        email=data.get("email"),
        service_type=data.get("service_type"),
        message=data.get("message"),
    )

    db.session.add(consultation)
    db.session.commit()

    return consultation


def get_consultation_success_response(consultation):
    """Get success response for consultation creation.

    Args:
        consultation: ConsultationRequest instance

    Returns:
        dict: Success response data
    """
    return {
        "success": True,
        "message": "Consultation request created successfully",
        "data": consultation.to_dict(),
    }


def get_consultation_error_response(message="Error creating consultation request"):
    """Get error response for consultation creation.

    Args:
        message: Error message

    Returns:
        dict: Error response data
    """
    return {"success": False, "message": message}
