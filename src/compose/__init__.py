from quart import Blueprint

compose_bp = Blueprint("compose", __name__, url_prefix="/compose")

from . import routes