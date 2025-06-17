"""Module docstring."""

from flask import jsonify, render_template, request


def register_error_handlers(app):
    """Function docstring."""

    @app.errorhandler(404)
    def not_found_error(error):
        """Function docstring."""
        if request.path.startswith("/api/"):
            return jsonify({"error": "Resource not found"}), 404
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Function docstring."""
        if request.path.startswith("/api/"):
            return jsonify({"error": "Internal server error"}), 500
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        """Function docstring."""
        if request.path.startswith("/api/"):
            return jsonify({"error": "Forbidden"}), 403
        return render_template("errors/403.html"), 403
