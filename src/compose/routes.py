from sqlalchemy import select
from datetime import datetime, timezone
from quart import render_template, request, redirect, url_for

from . import compose_bp
from database import async_session, Session as SessionModel


@compose_bp.route("/")
async def compose():
    current_ip = request.remote_addr
    current_ua = request.headers.get("User-Agent")
    current_session_token = request.cookies.get("alltale_biscuits")

    if not current_session_token:
        return redirect(url_for("login"))
    
    async with async_session() as db:
        result: SessionModel = await db.scalar(
            select().where(SessionModel.session_token == current_session_token)
        )

    if not result or result.expire_at < datetime.now(timezone.utc):
        return redirect(url_for("login"))

    ip_not_match = result.ip_address and result.ip_address != current_ip
    ua_not_match = result.user_agent and result.user_agent != current_ua

    if ip_not_match or ua_not_match:
        return redirect(url_for("login"))

    return await render_template("compose.html")