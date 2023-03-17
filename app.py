"""
Entrypoint to the application that conversion currency to EUR
"""
import sys
import json
import asyncio
import logging
import websockets
import time

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


async def ws_connect():
    """
    Connects to the websocket server and starts the heartbeat task
    """
    async with websockets.connect(config.WEBSOCKET_ENDPOINT) as websocket:
        logging.info("Connected to websocket server")

        async for message in websocket:
            while True:
                last_heartbeat = time.perf_counter()
                message = json.loads(message)
                if message["type"] == "heartbeat":
                    last_heartbeat = time.perf_counter()
                    await websocket.send(json.dumps({"type": "heartbeat"}))
                    logging.info("Sent back to the server heartbeat message")
                else:
                    message_task_result = await handle_message(message, rate_cache_handler)
                    if message_task_result:
                        await websocket.send(message_task_result)
                    logging.info("Message with converted data sent successfully")
                    continue

                if time.perf_counter() - last_heartbeat >= config.RECONNECT_DELAY:
                    logging.info("Raise error because the app didn't get heartbeat message during 2s")
                    raise Exception("The app didn't get heartbeat message during 2s")

                await asyncio.sleep(config.HEARTBEAT_INTERVAL)


async def main():
    while True:
        try:
            await ws_connect()
        except Exception:
            logging.error("Closed websocket and try reconnect to the websocket server")


if __name__ == "__main__":
    asyncio.run(main())
