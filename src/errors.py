
"""Error handlers for BaiMuras application."""

from flask import render_template, request, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register error handlers for the application.

    Args:
        app: Flask application instance
    """

    @app.errorhandler(400)
    def bad_request(error):  # pylint: disable=unused-argument
        """Handle 400 Bad Request errors."""
        app.logger.warning('Bad request: %s', request.url)

        if request.is_json:
            return jsonify({
                'error': 'Bad Request',
                'message': 'The request could not be understood by the server'
            }), 400

        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def unauthorized(error):  # pylint: disable=unused-argument
        """Handle 401 Unauthorized errors."""
        app.logger.warning('Unauthorized access: %s', request.url)

        if request.is_json:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required'
            }), 401

        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):  # pylint: disable=unused-argument
        """Handle 403 Forbidden errors."""
        app.logger.warning('Forbidden access: %s', request.url)

        if request.is_json:
            return jsonify({
                'error': 'Forbidden',
                'message': 'Access denied'
            }), 403

        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(error):  # pylint: disable=unused-argument
        """Handle 404 Not Found errors."""
        app.logger.info('Page not found: %s', request.url)

        if request.is_json:
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found'
            }), 404

        return render_template('errors/404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):  # pylint: disable=unused-argument
        """Handle 405 Method Not Allowed errors."""
        app.logger.warning('Method not allowed: %s %s', request.method, request.url)

        if request.is_json:
            return jsonify({
                'error': 'Method Not Allowed',
                'message': 'The method is not allowed for this resource'
            }), 405

        return render_template('errors/405.html'), 405

    @app.errorhandler(429)
    def rate_limit_exceeded(error):  # pylint: disable=unused-argument
        """Handle 429 Too Many Requests errors."""
        app.logger.warning('Rate limit exceeded: %s', request.url)

        if request.is_json:
            return jsonify({
                'error': 'Too Many Requests',
                'message': 'Rate limit exceeded. Please try again later'
            }), 429

        return render_template('errors/429.html'), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error('Internal server error: %s', str(error))

        if request.is_json:
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An internal server error occurred'
            }), 500

        return render_template('errors/500.html'), 500

    @app.errorhandler(502)
    def bad_gateway(error):
        """Handle 502 Bad Gateway errors."""
        app.logger.error('Bad gateway: %s', str(error))

        if request.is_json:
            return jsonify({
                'error': 'Bad Gateway',
                'message': 'Bad gateway error occurred'
            }), 502

        return render_template('errors/502.html'), 502

    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable errors."""
        app.logger.error('Service unavailable: %s', str(error))

        if request.is_json:
            return jsonify({
                'error': 'Service Unavailable',
                'message': 'Service temporarily unavailable'
            }), 503

        return render_template('errors/503.html'), 503

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle unexpected exceptions."""
        if isinstance(error, HTTPException):
            return error

        app.logger.error('Unexpected error: %s', str(error))

        if request.is_json:
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }), 500

        return render_template('errors/500.html'), 500
