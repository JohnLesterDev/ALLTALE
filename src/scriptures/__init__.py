from quart import Blueprint

scriptures_bp = Blueprint("scriptures", __name__, url_prefix="/scriptures")

from . import routes