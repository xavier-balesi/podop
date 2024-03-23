import asyncio
import logging
from typing import TYPE_CHECKING

from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect

from back.config import ApiConfig, ApplicationConfig
from back.controllers.game import Game

if TYPE_CHECKING:
    from back.models.counts_history import CountsHistory

log = logging.getLogger(__name__)


app = FastAPI()
api_config: ApiConfig = ApplicationConfig().api


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Start a new game by connecting to a websocket.

    The game runs as fast as possible. Eventually slow it down by using the `turn_interval` config.
    Spying the game by sampling the game resources at a given framerate (see `framerate` config).
    Game information are communicated in JSON format by a websocket.
    A complete resource history is sent when the game is over.
    """
    log.info("Client connected")
    await websocket.accept()
    game = Game()

    async def notify_front() -> None:
        while game.running:
            await asyncio.sleep(1.0 / api_config.framerate)

            # Sampling number of game resources on each frame.
            front_msg: str = game.get_counts().json()
            try:
                # Using a websocket to eventually pilot the trading strategy manually from the web client.
                await websocket.send_text(front_msg)
            except WebSocketDisconnect as e:
                log.warning(f"Client disconnected: {e!r}", exc_info=True)
                return

        # Send the complete resource history when the game is over.
        counts_history: CountsHistory = game.get_counts_history()
        # TODO: timeit orjson.dumps(model.dict(exclude_none=True))
        front_msg = counts_history.json(exclude_none=True)
        # We can also debug the backend without frontend by doing:
        #   python -m websockets 'ws://localhost:8080/ws'
        # and displaying the desired data in color with:
        #   print_json(data=counts_history.dict(exclude_none=True))
        # from rich module, for example.
        try:
            await websocket.send_text(front_msg)
        except WebSocketDisconnect as e:
            log.warning(f"Client disconnected: {e!r}", exc_info=True)
            return

    # Run the game and spy the game in parallel, by sampling the inventory.
    await asyncio.gather(game.run(), notify_front())
