"""
Entrypoint to the application that conversion currency to EUR
"""
import json
import asyncio
import logging
import websockets
import time

from exchangerateconversion.config import config
from exchangerateconversion.handler_msg import handle_message


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s()] - %(message)s",
    datefmt="%H:%M:%S",
    filename="app.log",
    level=logging.INFO,
)


async def main():
    """
    Connects to the websocket server and starts the heartbeat task
    """
    while True:
        try:
            async with websockets.connect(config.WEBSOCKET_ENDPOINT) as websocket:
                logging.info("Connected to websocket server")

                async for message in websocket:
                    last_heartbeat = time.perf_counter()
                    message = json.loads(message)
                    if message["type"] == "heartbeat":
                        last_heartbeat = time.perf_counter()
                        logging.info("Sent back to the server heartbeat message")
                        await websocket.send(json.dumps({"type": "heartbeat"}))
                    else:
                        message_task_result = await asyncio.create_task(handle_message(message))
                        if message_task_result:
                            await websocket.send(message_task_result)
                        logging.info("Message with converted data sent successfully")
                        continue

                    if time.perf_counter() - last_heartbeat >= config.RECONNECT_DELAY:
                        logging.info("Raise error because the app didn't get heartbeat message during 2s")
                        raise

                    await asyncio.sleep(config.HEARTBEAT_INTERVAL)

        except Exception:
            logging.info("Closing websocket connection...")
            logging.info("Trying to reconnect...")


if __name__ == "__main__":
    asyncio.run(main())
