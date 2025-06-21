"""Utility functions for BaiMuras application."""

import re

from flask import request, session


def get_current_language():
    """Get current language from session or request headers."""
    # Check session first
    if "language" in session:
        return session["language"]

    # Check Accept-Language header
    if request and hasattr(request, "headers"):
        accept_language = request.headers.get("Accept-Language", "")
        if "ky" in accept_language.lower():
            return "ky"

    # Default to Russian
    return "ru"


def get_app_version():
    """Get application version from VERSION file."""
    try:
        with open("VERSION", "r", encoding="utf-8") as version_file:
            return version_file.read().strip()
    except FileNotFoundError:
        return "1.0.0"


def validate_phone_number(phone):
    """Validate phone number format."""
    if not phone:
        return False

    # Remove all non-digit characters
    clean_phone = re.sub(r"\D", "", phone)

    # Check if it's a valid Kyrgyzstan phone number
    # Kyrgyzstan numbers: +996XXXXXXXXX (12 digits total)
    if len(clean_phone) == 12 and clean_phone.startswith("996"):
        return True

    # Also accept local format: 0XXXXXXXXX (10 digits)
    if len(clean_phone) == 10 and clean_phone.startswith("0"):
        return True

    return False


def validate_email(email):
    """Validate email format."""
    if not email:
        return True  # Email is optional

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))


def sanitize_input(text):
    """Sanitize user input to prevent XSS."""
    if not text:
        return ""

    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", '"', "'", "&"]
    for char in dangerous_chars:
        text = text.replace(char, "")

    return text.strip()


def format_phone_display(phone):
    """Format phone number for display."""
    if not phone:
        return ""

    # Remove all non-digit characters
    clean_phone = re.sub(r"\D", "", phone)

    # Format Kyrgyzstan number
    if len(clean_phone) == 12 and clean_phone.startswith("996"):
        return f"+{clean_phone[:3]} {clean_phone[3:6]} {clean_phone[6:9]} {clean_phone[9:]}"

    # Format local number
    if len(clean_phone) == 10:
        return f"{clean_phone[:4]} {clean_phone[4:7]} {clean_phone[7:]}"

    return phone
