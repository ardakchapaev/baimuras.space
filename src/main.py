import os
import sys
import datetime # Import datetime
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, session
from src.routes.main_routes import main_bp
from src.routes.user import user_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'), template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(24)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)

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
