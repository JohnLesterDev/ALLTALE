import asyncio
from quart import Quart, jsonify
from database import engine, async_session, Base, init_db
from database import Passage, Prayer, PassageBibleLink, Seal, PassageSeal

app = Quart(__name__, static_folder="res", template_folder="temps")



if __name__ == "__main__":
    asyncio.run(init_db())
    app.run(host="0.0.0.0", port=8080)
