import asyncio
import logging

from fastapi import FastAPI
from rich import print_json
from starlette.websockets import WebSocket, WebSocketDisconnect

from back.config import ApiConfig, ApplicationConfig
from back.controllers.game import Game
from back.models.counts_history import CountsHistory

log = logging.getLogger(__name__)


app = FastAPI()
api_config: ApiConfig = ApplicationConfig().api


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    log.info("Client connected")
    await websocket.accept()
    game = Game()

    async def notify_front():
        trn_sent_count = 0
        while game.running:
            await asyncio.sleep(1 / api_config.framerate)
            # Using a websocket to eventually pilot the trading strategy manually from the web client.
            new_counts_history: CountsHistory = game.get_counts_history()[
                trn_sent_count:
            ]
            trn_sent_count += len(new_counts_history)
            # TODO: timeit orjson.dumps(model.dict(exclude_none=True))
            front_msg: str = new_counts_history.json(exclude_none=True)
            print_json(data=new_counts_history.dict(exclude_none=True))
            # breakpoint()
            try:
                await websocket.send_text(front_msg)
            except WebSocketDisconnect as e:
                log.warning(f"Client disconnected: {e!r}", exc_info=True)
                return

    await asyncio.gather(game.run(), notify_front())
