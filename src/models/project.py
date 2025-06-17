
from datetime import datetime
from src.models.user import db

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_type = db.Column(db.String(100), nullable=True)  # furniture, design, academy
    status = db.Column(db.String(50), default='planning')  # planning, in_progress, completed, cancelled
    budget = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с лидом
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    
    def __repr__(self):
        return f'<Project {self.title} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'project_type': self.project_type,
            'status': self.status,
            'budget': self.budget,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'lead_id': self.lead_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
