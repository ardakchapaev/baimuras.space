# BaiMuras Website

BaiMuras is a demonstration website for a furniture design studio. The project shows how to structure a small Flask application with multiple pages, a basic dashboard and an example REST API. The current code base focuses on presenting content and experimenting with templates and styling.

## Features

- Main pages: home, about, services (including custom furniture, design bureau and academy), portfolio, blog and contact form.
- Simple dashboard with authentication and pages for leads, analytics and settings.
- Contact form with flash messages.
- Example REST API for managing users (create, read, update, delete).
- Styling built on Bootstrap 5 with custom CSS and Jinja2 templates.

## Technologies

- Python 3
- [Flask](https://flask.palletsprojects.com/) and Blueprints
- Jinja2 template engine
- Bootstrap 5 for UI
- Flask‑SQLAlchemy (only basic setup for the `User` model)

## Installation and usage

1. **Create a virtual environment and install dependencies**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**:

   - `SECRET_KEY` – by default a random key is generated each time the app starts. You can set a persistent key via environment variable:
     ```bash
     export SECRET_KEY="your-secret-key"
     ```
   - `SQLALCHEMY_DATABASE_URI` – set this if you plan to use the REST API with a database. Example for SQLite:
     ```bash
     export SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
     ```
   After configuring the URI you need to initialize the database manually (for example using Flask shell).

3. **Run the application**:

   ```bash
   FLASK_APP=wsgi.py flask run
   ```
   Or simply `python wsgi.py` for a basic development server.

## Roadmap

The project is a work in progress. Planned improvements include:

- Integration of a real database for storing users and contact messages.
- Admin features for managing blog posts and portfolio items.
- Deployment instructions and Docker support.

