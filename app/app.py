from flask import Flask, render_template

from app.extensions import csrf_protect, login_manager, migrate, bootstrap, db
from app.main import blueprint as main_bp
from config import Config


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(main_bp)
    return None
