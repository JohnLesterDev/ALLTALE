from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from quart import render_template, request, redirect, url_for

from . import compose_bp
from database import async_session, Session as SessionModel


@compose_bp.route("/")
async def compose():
    current_ip: str = request.remote_addr or ""
    current_ua: str = request.headers.get("User-Agent") or ""
    current_session_token: str | None = request.cookies.get("alltale_biscuits")

    if not current_session_token:
        return redirect(url_for("login.login_get", sunod=request.path))

    async with async_session() as db:
        stmt = select(SessionModel).options(selectinload(SessionModel.user)).where(
            SessionModel.session_token == current_session_token
            )
        result: SessionModel | None = await db.scalar(stmt)

        if (
            not result
            or not result.user_id
            or not result.user.is_active  
            or result.expire_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc)
            or (result.ip_address and result.ip_address != current_ip) 
            or (result.user_agent and result.user_agent != current_ua)
        ):
            return redirect(url_for("login.login_get", sunod=request.path))

    return await render_template("compose.html")