from quart import Blueprint

login_bp = Blueprint("login", __name__, url_prefix="/login")

from . import routes