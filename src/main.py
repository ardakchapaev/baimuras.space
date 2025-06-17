import os
import sys
import datetime # Import datetime
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, session
from src.routes.main_routes import main_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'), template_folder='templates')
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    if os.environ.get("FLASK_ENV") == "production":
        raise RuntimeError("SECRET_KEY environment variable must be set in production")
    secret_key = os.urandom(24)
    print(
        "WARNING: SECRET_KEY not set. Using a generated key for development only",
        file=sys.stderr,
    )
app.config["SECRET_KEY"] = secret_key

# Register blueprints
app.register_blueprint(main_bp)

# Make session and current_year available to all templates
@app.context_processor
def inject_global_vars():
    return dict(session=session, current_year=datetime.datetime.utcnow().year)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/health")
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
