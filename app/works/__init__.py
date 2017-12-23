from flask import Blueprint

works = Blueprint('works', __name__)

from . import views
