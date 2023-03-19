"""
Entrypoint to the application that conversion currency to EUR
"""
import sys
import json
import asyncio
import logging
import websockets

from exchangerateconversion.config import config
from exchangerateconversion.handler_msg import handle_message
from exchangerateconversion.fetch import FetchExchangeRateWithCache


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s()] - %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("app.log")],
    level=logging.INFO,
)

rate_cache_handler = FetchExchangeRateWithCache()


async def heartbeat(ws):
    while True:
        logging.info("Sent back to the server heartbeat message")
        await ws.send(json.dumps({"type": "heartbeat"}))
        await asyncio.sleep(config.HEARTBEAT_INTERVAL)


async def ws_connect():
    """
    Connects to the websocket server and starts the heartbeat task
    """
    while True:
        try:
            async with websockets.connect(config.WEBSOCKET_ENDPOINT) as websocket:
                logging.info("Connected to websocket server")

                asyncio.create_task(heartbeat(websocket))
                while True:
                    message = await asyncio.wait_for(websocket.recv(), timeout=config.RECONNECT_DELAY)
                    message = json.loads(message)

                    if message["type"] == "message":
                        asyncio.create_task(handle_message(message, rate_cache_handler, websocket))
        except (Exception, websockets.exceptions.ConnectionClosedOK):
            logging.error("Closed websocket and try reconnect to the websocket server again")


if __name__ == "__main__":
    asyncio.run(ws_connect())
