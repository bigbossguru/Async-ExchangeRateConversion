from pydantic import BaseSettings


class Config(BaseSettings):
    """
    The general configuration file for main app
    """

    WEBSOCKET_ENDPOINT: str = "wss://currency-assignment.ematiq.com"
    EXCHANGE_RATE_API: str = "https://api.exchangerate.host"
    EXPIRE_CACHE_TIME: int = 7200  # 2h in the seconds
    HEARTBEAT_INTERVAL: int = 1  # seconds
    RECONNECT_DELAY: int = 2  # seconds


config = Config()
