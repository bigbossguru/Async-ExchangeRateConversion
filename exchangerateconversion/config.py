import json
from datetime import timedelta
from pydantic import BaseSettings


class Config(BaseSettings):
    """
    The general configuration file for main app
    """

    WEBSOCKET_ENDPOINT: str = "wss://currency-assignment.ematiq.com"
    EXCHANGE_RATE_API: str = "https://api.exchangerate.host"
    HEARTBEAT_MESSAGE: str = json.dumps({"type": "heartbeat"})
    EXPIRE_CACHE_TIME: timedelta = timedelta(hours=2)

    HEARTBEAT_INTERVAL: int = 1  # seconds
    RECONNECT_DELAY: int = 2  # seconds


config = Config()
