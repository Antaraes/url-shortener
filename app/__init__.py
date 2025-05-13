from datetime import datetime
from flask import Flask
from app.config import config
from app.extensions import db, migrate, csrf

def create_app(config_name='development'):
    """
    Application factory function to create and configure the Flask app.
    
    Args:
        config_name (str): Configuration environment to use
        
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Register blueprints
    from app.api.routes import api_bp
    from app.web.routes import web_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    @app.template_filter('datetime')
    def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
        """Format a datetime object."""
        if value is None:
            return ""
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                return value
        return value.strftime(format)
    
    return app