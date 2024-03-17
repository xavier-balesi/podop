import asyncio
import logging

from fastapi import FastAPI
from orjson import orjson
from starlette.websockets import WebSocket, WebSocketDisconnect

from back.config import ApiConfig, ApplicationConfig
from back.controllers.game import Game

log = logging.getLogger(__name__)


app = FastAPI()
api_config: ApiConfig = ApplicationConfig().api


# sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Vous pouvez ajuster ceci selon vos besoins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    log.info("Client connected")
    await websocket.accept()
    game = Game()

    async def notify_front():
        try:
            while game.running:
                await asyncio.sleep(1 / api_config.framerate)
                # using a websocket to eventually pilot the trading strategy manually from the web client
                await websocket.send_text(
                    orjson.dumps(game.get_stats()).decode("utf-8")
                )
        except WebSocketDisconnect as e:
            log.warning(f"Client disconnected: {e!r}", exc_info=True)

    await asyncio.gather(game.run(), notify_front())


# @sio.on("sio")
# async def puzzle_duel(sid, msg):
#     print("connect", sid)
#     data = orjson.loads(msg)
#     print(data)
#
#
# app.mount("/", socketio.ASGIApp(sio))
