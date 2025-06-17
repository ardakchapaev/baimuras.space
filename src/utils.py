
"""Utility functions for BaiMuras application."""

from flask import session, request
from src.config import Config


def get_current_language():
    """Get current language from session or default."""
    return session.get('language', Config.DEFAULT_LANGUAGE)


def set_language(language):
    """Set language in session."""
    if language in Config.LANGUAGES:
        session['language'] = language
        return True
    return False


def get_localized_content(content_dict):
    """Get content in current language."""
    current_lang = get_current_language()
    return content_dict.get(current_lang, content_dict.get(Config.DEFAULT_LANGUAGE, ''))


def is_mobile():
    """Check if request is from mobile device."""
    user_agent = request.headers.get('User-Agent', '').lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'tablet']
    return any(keyword in user_agent for keyword in mobile_keywords)


def format_phone(phone):
    """Format phone number for display."""
    if not phone:
        return ''
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) >= 10:
        return f"+{digits[:3]} ({digits[3:6]}) {digits[6:9]}-{digits[9:]}"
    return phone


def generate_slug(text):
    """Generate URL-friendly slug from text."""
    import re
    import unicodedata
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ascii characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase and replace spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    return text
