import asyncio
import json
import logging
import websockets

from .config import config
from .converter import convert_stake


async def heartbeat(websocket: websockets.WebSocketClientProtocol) -> None:  # type: ignore
    """
    Send heartbeat messages to the websocket server every second.
    """
    while True:
        await asyncio.sleep(config.HEARTBEAT_INTERVAL)
        try:
            await websocket.send(config.HEARTBEAT_MESSAGE)
        except Exception as e:
            logging.error(f"Unable to send heartbeat. Error: {e}")
            break


async def websocket_connection() -> None:
    """
    Connects to the WebSocket server and listens for messages
    """
    while True:
        try:
            async with websockets.connect(config.WEBSOCKET_ENDPOINT) as websocket:  # type: ignore
                logging.info("Connected to server")
                asyncio.create_task(heartbeat(websocket))

                async for message in websocket:
                    message = json.loads(message)
                    if message.get("type") == "message":
                        logging.info("Converting the currency")
                        converted = await convert_stake(message)
                        logging.info(f"Converted result: {json.dumps(converted)}")
                        await websocket.send(json.dumps(converted))

        except Exception as e:
            logging.error(f"Error connecting to server. Retrying in 2 seconds. Error: {e}")
            await asyncio.sleep(config.RECONNECT_DELAY)
