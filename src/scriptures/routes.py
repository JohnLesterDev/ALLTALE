from quart import render_template
from . import scriptures_bp

@scriptures_bp.route("/")
async def scriptures():
    return await render_template("scriptures.html")