from flask import Blueprint

blueprint = Blueprint('main', __name__, template_folder='../templates', static_folder='../static')

from app.main import views
