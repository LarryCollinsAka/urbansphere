import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Load global state from our new globals.py module ---
# This line will trigger the loading of all configs and knowledge bases.
import globals as app_globals

# --- Register Routers ---
# Now we import the Blueprints without causing a circular dependency
from routers.main_routes import main_bp
from routers.api_routes import api_bp
from routers.webhook_routes import webhook_bp

app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(webhook_bp, url_prefix='/webhook')

# --- Main Entry Point ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
