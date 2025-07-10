from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager

from .config import config

# --- Extension Initialization ---
# These are initialized here but configured in the factory
# to avoid circular imports and to bind them to a specific app instance.
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
# This defines the view that users are redirected to when they try to
# access a page that requires them to be logged in.
login_manager.login_view = 'auth.login' 

# The Admin extension is initialized here
admin = Admin(name='Flask-Commerce Admin', template_mode='bootstrap3')


def create_app(config_name: str):
    """
    An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_name: The name of the configuration to use.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # --- Register Extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    admin.init_app(app)

    # --- Blueprints Registration ---
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # from .api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app 