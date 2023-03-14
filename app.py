"""
Entrypoint to the application that conversion currency to EUR
"""
import json
import asyncio
import logging
import websockets

from exchangerateconversion.config import config
from exchangerateconversion.handler_msg import handle_message, send_heartbeat


logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    filename="app.log",
    level=logging.INFO,
)


async def main():
    while True:
        try:
            async with websockets.connect(config.WEBSOCKET_ENDPOINT) as websocket:
                logging.debug("Connected to websocket")
                async for message in websocket:
                    message_data = json.loads(message)
                    tasks = [
                        asyncio.ensure_future(handle_message(message_data)),
                        asyncio.ensure_future(send_heartbeat(websocket)),
                    ]
                    done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                    for task in done:
                        result = task.result()
                        if result is not None:
                            await websocket.send(result)
        except Exception:
            logging.error("Error connecting to server. Retrying in 2 seconds")
        await asyncio.sleep(config.RECONNECT_DELAY)


if __name__ == "__main__":
    asyncio.run(main())
