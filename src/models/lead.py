"""Module docstring."""

from datetime import datetime

from . import db


class Lead(db.Model):
    """Class docstring."""

    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(50), default="new"
    )  # new, contacted, qualified, converted, lost
    score = db.Column(db.Float, default=0.0)  # Lead scoring 0-1
    source = db.Column(
        db.String(100), nullable=True
    )  # website, telegram, referral, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Связь с проектами
    projects = db.relationship("Project", backref="lead", lazy=True)

    def __repr__(self):
        """Function docstring."""
        return f"<Lead {self.name} - {self.status}>"

    def to_dict(self):
        """Function docstring."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "subject": self.subject,
            "message": self.message,
            "status": self.status,
            "score": self.score,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
