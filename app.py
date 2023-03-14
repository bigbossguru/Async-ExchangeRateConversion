"""
Entrypoint to the application that conversion currency to EUR
"""
import asyncio
import logging

from exchangerateconversion.ws_connection import websocket_connection


logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    filename="app.log",
    level=logging.INFO,
)


if __name__ == "__main__":
    asyncio.run(websocket_connection())
