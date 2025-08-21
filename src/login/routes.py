import bcrypt
import secrets

from sqlalchemy import select
from quart import Response, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timezone, timedelta
from typing import Optional

from . import login_bp
from database import async_session, Session as SessionModel, User as UserModel



@login_bp.route("/", methods=["GET"])
async def login_get():
    curr_session_token = request.cookies.get("alltale_biscuits")

    async with async_session() as db:
        csrf_token = None
        session_row: Optional[SessionModel] = None

        if curr_session_token:
            stmt = select(SessionModel).where(SessionModel.session_token == curr_session_token)
            session_row = await db.scalar(stmt)

            if session_row and session_row.expire_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                session_row = None

        if session_row and session_row.csrf_token:
            csrf_token = session_row.csrf_token
        else:
            csrf_token = secrets.token_urlsafe(32)
            temp_session = SessionModel(
                user_id=None,
                session_token=secrets.token_urlsafe(32),
                expire_at=datetime.now(timezone.utc) + timedelta(minutes=5),
                csrf_token=csrf_token
            )

            db.add(temp_session)
            await db.commit()

            session_row = temp_session

    html = await render_template("login.html", csrf_token=csrf_token)
    response = Response(html, status=200)
    response.set_cookie(
        "alltale_biscuits", 
        session_row.session_token, 
        max_age=3600, 
        samesite="Lax",
        httponly=True
        )
    
    return response


@login_bp.route("/", methods=["POST"])
async def login_post():
    form = await request.form

    username = form.get("username", "").strip()
    password = form.get("password", "")
    csrf_token = form.get("csrf_token", "")

    curr_session_token = request.cookies.get("alltale_biscuits")

    if csrf_token and not curr_session_token:
        return jsonify({"success": False, "message": "Unable to process request."}), 403
    
    async with async_session() as db:
        session_row: Optional[SessionModel] = None

        if curr_session_token:
            stmt = select(SessionModel).where(SessionModel.session_token == curr_session_token)    
            session_row = await db.scalar(stmt)

            if session_row and session_row.expire_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                session_row = None

        if not session_row or not csrf_token or csrf_token != getattr(session_row, "csrf_token", None):
            return jsonify({"success": False, "message": "Unable to process login request."}), 403
        
        stmt = select(UserModel).where(UserModel.username == username)
        user = await db.scalar(stmt)

        if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return jsonify({"success": False, "message": "Incorrect username or password."}), 403

        new_alltale_biscuits = secrets.token_urlsafe(32)
        session_row.session_token = new_alltale_biscuits
        session_row.expire_at = datetime.now(timezone.utc) + timedelta(hours=1)
        session_row.csrf_token = secrets.token_urlsafe(32)
        session_row.user_id = user.id
        session_row.ip_address = request.remote_addr
        session_row.user_agent = request.headers.get("User-Agent")

        await db.commit()
        await db.refresh(session_row)

        return jsonify({
            "success": True,
            "session_token": new_alltale_biscuits,
            "csrf_token": session_row.csrf_token
            }), 200
