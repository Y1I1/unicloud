from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import sentry_sdk
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import os
from sentry_sdk.integrations.flask import FlaskIntegration

# Create extensions as module-level variables
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    csrf.init_app(app)
    
    login.login_view = 'main.login'

    # Sentry initialization (only if DSN is set)
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0
        )

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return "404 Not Found", 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return "500 Internal Server Error", 500

    @app.errorhandler(401)
    def unauthorized_error(error):
        return "401 Unauthorized", 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return "403 Forbidden", 403

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return "422 Unprocessable Entity", 422

    # from app import models  # Removed to fix circular import
    from app.routes import main_bp, admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Import models after app creation to avoid circular imports
    from app import models
    
    @login.user_loader
    def load_user(id):
        return models.User.query.get(int(id))
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 