
"""Consultation request model for BaiMuras application."""

from datetime import datetime
from . import db


class ConsultationRequest(db.Model):
    """Model for consultation requests."""

    __tablename__ = 'consultation_requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    service_type = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')

    def __repr__(self):
        """String representation of consultation request."""
        return f'<ConsultationRequest {self.name}: {self.service_type}>'

    def to_dict(self):
        """Convert consultation request to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'service_type': self.service_type,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'status': self.status
        }
