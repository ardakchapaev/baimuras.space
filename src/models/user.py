"""Module docstring."""

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .role import roles_users


class User(db.Model):
    """Class docstring."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref("users", lazy="dynamic"),
    )

    def __repr__(self):
        """Function docstring."""
        return f"<User {self.username}>"

    def set_password(self, password: str) -> None:
        """Hash and store the given password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Return True if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Function docstring."""
        return {"id": self.id, "username": self.username, "email": self.email}
