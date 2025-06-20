"""Database models package."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .role import Role, roles_users  # noqa: E402
from .user import User  # noqa: E402
from .lead import Lead  # noqa: E402
from .project import Project  # noqa: E402
from .consultation import ConsultationRequest  # noqa: E402

__all__ = [
    "db",
    "User",
    "Lead",
    "Project",
    "Role",
    "ConsultationRequest",
    "roles_users",
]
