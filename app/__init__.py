from flask import Flask
from .models import db  # Import db from models.py
from .routes import bp as main_bp
from .schemas import SHEETS, HEADER_HINTS

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    
    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:test%40123@localhost:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "Saltriver@123"
    
    print("USING DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    
    # Initialize database with app
    db.init_app(app)
    
    # Make SHEETS and HEADER_HINTS available in templates
    app.jinja_env.globals["SHEETS"] = SHEETS
    app.jinja_env.globals["HEADER_HINTS"] = HEADER_HINTS
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
