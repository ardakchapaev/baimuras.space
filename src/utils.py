
"""Utility functions for the BaiMuras application.

This module contains helper functions used throughout the application.
"""

import os
from typing import Optional
from flask import session, request


def get_current_language() -> str:
    """Get the current language from session or request.
    
    Returns:
        str: Current language code ('ru' or 'ky').
    """
    # Check session first
    if 'language' in session:
        return session['language']
    
    # Check Accept-Language header
    if request and hasattr(request, 'accept_languages'):
        best_match = request.accept_languages.best_match(['ru', 'ky'])
        if best_match:
            return best_match
    
    # Default to Russian
    return 'ru'


def get_app_version() -> str:
    """Get application version from version file.
    
    Returns:
        str: Application version string.
    """
    try:
        version_file = os.path.join(os.path.dirname(__file__), 'version.py')
        if os.path.exists(version_file):
            with open(version_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # Extract version from __version__ = "x.x.x" format
                if '__version__' in content:
                    version_line = [line for line in content.split('\n') 
                                  if line.strip().startswith('__version__')][0]
                    return version_line.split('=')[1].strip().strip('"\'')
                return content
        return "1.0.0"
    except Exception:
        return "1.0.0"


def allowed_file(filename: str, allowed_extensions: Optional[set] = None) -> bool:
    """Check if a file has an allowed extension.
    
    Args:
        filename: Name of the file to check.
        allowed_extensions: Set of allowed extensions. If None, uses default set.
        
    Returns:
        bool: True if file extension is allowed, False otherwise.
    """
    if allowed_extensions is None:
        allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
    
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in allowed_extensions)


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe storage.
    
    Args:
        filename: Original filename.
        
    Returns:
        str: Sanitized filename.
    """
    # Remove or replace dangerous characters
    import re
    # Keep only alphanumeric, dots, hyphens, and underscores
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Limit length
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext
    return sanitized
