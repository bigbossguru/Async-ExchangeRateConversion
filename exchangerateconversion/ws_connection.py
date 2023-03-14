from datetime import datetime
import asyncio
import json
import logging
import websockets

from .config import config
from .fetch_rate import get_exchange_rate, ExchangeException
from .converter import convert_stake


async def websocket_connection() -> None:
    """
    Connects to the WebSocket server and listens for messages
    """
    while True:
        try:
            async with websockets.connect(config.WEBSOCKET_ENDPOINT) as websocket:  # type: ignore
                logging.info("Connected to server")

                async for message in websocket:
                    message = json.loads(message)
                    if message.get("type") == "message":
                        try:
                            logging.info("Converting the currency")
                            currency = message["payload"]["currency"]
                            date = datetime.fromisoformat(message["payload"]["date"])

                            # Get currency rate from external API
                            currency_rate = await get_exchange_rate(currency, date)

                            # Converts the stake in the given message to EUR according to the exchange rate
                            message = convert_stake(message, currency_rate)

                            logging.info(f"Converted result: {json.dumps(message)}")
                        except ExchangeException as e:
                            message = {"type": "error", "id": message["id"], "message": str(e)}
                        await websocket.send(json.dumps(message))
                    else:
                        await websocket.send(config.HEARTBEAT_MESSAGE)
                        await asyncio.sleep(config.HEARTBEAT_INTERVAL)

        except Exception as e:
            logging.error(f"Error connecting to server. Retrying in 2 seconds. Error: {e}")
        await asyncio.sleep(config.RECONNECT_DELAY)
