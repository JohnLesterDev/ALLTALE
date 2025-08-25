from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

import os
import asyncio

from quart import Quart, render_template

from database import engine, async_session, Base, init_db
from database import Passage, Prayer, PassageBibleLink, Seal, PassageSeal

from login.routes import login_bp
from compose.routes import compose_bp


app = Quart(
    __name__, 
    static_folder=os.path.join(BASE_DIR, "res"),
    static_url_path="/res",
    template_folder=os.path.join(BASE_DIR, "temps")
    )

app.config["SECRET_KEY"] = os.getenv("ALLTALE_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'alltale_biscuits'
app.config['SESSION_COOKIE_HTTPONLY'] = True     
app.config['SESSION_COOKIE_SECURE'] = False       
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'     

app.register_blueprint(login_bp)
app.register_blueprint(compose_bp)


@app.route("/")
async def root_route():
    return await render_template("home.html")

@app.errorhandler(404)
async def page_not_found(e):
    return await render_template("errors/404.html"), 404


if __name__ == "__main__":
    asyncio.run(init_db())
    app.run(host="0.0.0.0", port=8080, debug=True)
