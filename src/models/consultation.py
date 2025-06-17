
"""Consultation request model."""

from datetime import datetime
from src.models.user import db


class ConsultationRequest(db.Model):
    """Model for consultation requests."""
    
    __tablename__ = 'consultation_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    service_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    language = db.Column(db.String(2), default='ru')
    status = db.Column(db.String(20), default='new')  # new, contacted, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConsultationRequest {self.name} - {self.service_type}>'
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'service_type': self.service_type,
            'message': self.message,
            'language': self.language,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
