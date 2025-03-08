from flask import Flask
from .main import main_bp
import os

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath('templates'))
    app.register_blueprint(main_bp)
    return app