#-*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory in app.  py"""
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
migrate = Migrate()
csrf_protect = CSRFProtect()
login_manager = LoginManager()
bootstrap = Bootstrap()
