# BaiMuras Website

This repository contains a simple Flask-based website for BaiMuras. You can run it locally using Python.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set the `SECRET_KEY` environment variable** before starting the application. This is required in production to keep sessions secure. You can generate a key with Python:
   ```bash
   export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
   ```

## Running

Run the application with:
```bash
python wsgi.py
```

During development, if `SECRET_KEY` is not set, the app will generate a temporary key and display a warning. In production, the application will fail to start without `SECRET_KEY`.
