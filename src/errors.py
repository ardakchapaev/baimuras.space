
"""Error handlers for the BaiMuras application.

This module provides centralized error handling with proper logging
and user-friendly error pages.
"""

import logging
from typing import Tuple, Any

from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Register error handlers for the Flask application.
    
    Args:
        app: Flask application instance.
    """
    
    @app.errorhandler(400)
    def bad_request(error: HTTPException) -> Tuple[Any, int]:
        """Handle 400 Bad Request errors.
        
        Args:
            error: The HTTP exception.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        logger.warning(f"Bad request from {request.remote_addr}: {error}")
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Request',
                'message': 'The request could not be understood by the server.'
            }), 400
        
        try:
            return render_template('errors/400.html'), 400
        except Exception as e:
            logger.error(f"Error rendering 400 template: {e}")
            return "Bad Request", 400

    @app.errorhandler(401)
    def unauthorized(error: HTTPException) -> Tuple[Any, int]:
        """Handle 401 Unauthorized errors.
        
        Args:
            error: The HTTP exception.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        logger.warning(f"Unauthorized access attempt from {request.remote_addr}: {error}")
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication is required to access this resource.'
            }), 401
        
        try:
            return render_template('errors/401.html'), 401
        except Exception as e:
            logger.error(f"Error rendering 401 template: {e}")
            return "Unauthorized", 401

    @app.errorhandler(403)
    def forbidden(error: HTTPException) -> Tuple[Any, int]:
        """Handle 403 Forbidden errors.
        
        Args:
            error: The HTTP exception.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        logger.warning(f"Forbidden access attempt from {request.remote_addr}: {error}")
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'You do not have permission to access this resource.'
            }), 403
        
        try:
            return render_template('errors/403.html'), 403
        except Exception as e:
            logger.error(f"Error rendering 403 template: {e}")
            return "Forbidden", 403

    @app.errorhandler(404)
    def not_found(error: HTTPException) -> Tuple[Any, int]:
        """Handle 404 Not Found errors.
        
        Args:
            error: The HTTP exception.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        logger.info(f"404 error for {request.url} from {request.remote_addr}")
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found.'
            }), 404
        
        try:
            return render_template('errors/404.html'), 404
        except Exception as e:
            logger.error(f"Error rendering 404 template: {e}")
            return "Page Not Found", 404

    @app.errorhandler(500)
    def internal_error(error: Exception) -> Tuple[Any, int]:
        """Handle 500 Internal Server Error.
        
        Args:
            error: The exception that caused the error.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        logger.error(f"Internal server error: {error}", exc_info=True)
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred. Please try again later.'
            }), 500
        
        try:
            return render_template('errors/500.html'), 500
        except Exception as e:
            logger.error(f"Error rendering 500 template: {e}")
            return "Internal Server Error", 500

    @app.errorhandler(503)
    def service_unavailable(error: HTTPException) -> Tuple[Any, int]:
        """Handle 503 Service Unavailable errors.
        
        Args:
            error: The HTTP exception.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        logger.error(f"Service unavailable: {error}")
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Service Unavailable',
                'message': 'The service is temporarily unavailable. Please try again later.'
            }), 503
        
        try:
            return render_template('errors/503.html'), 503
        except Exception as e:
            logger.error(f"Error rendering 503 template: {e}")
            return "Service Unavailable", 503

    @app.errorhandler(Exception)
    def handle_exception(error: Exception) -> Tuple[Any, int]:
        """Handle unexpected exceptions.
        
        Args:
            error: The exception that occurred.
            
        Returns:
            Tuple[Any, int]: Error response and status code.
        """
        # Pass through HTTP errors
        if isinstance(error, HTTPException):
            return error
        
        # Log the error
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred. Please try again later.'
            }), 500
        
        try:
            return render_template('errors/500.html'), 500
        except Exception as e:
            logger.error(f"Error rendering 500 template: {e}")
            return "Internal Server Error", 500
