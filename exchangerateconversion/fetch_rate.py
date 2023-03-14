from typing import Dict, Tuple
from datetime import datetime
import aiohttp

from .config import config


CURRENCY_RATE_CACHE: Dict[str, Tuple[float, datetime]] = {}  # {currency: (rate, expiration)}


class ExchangeException(Exception):
    """
    Exception say about unable to get exchange rate
    """


async def get_exchange_rate(currency: str, date: datetime) -> float:
    """
    Fetches the exchange rate for the given currency and date from the API.
    """
    if currency in CURRENCY_RATE_CACHE:
        rate, expiration = CURRENCY_RATE_CACHE[currency]
        if datetime.now() < expiration:
            return rate

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{config.EXCHANGE_RATE_API}/convert?date={date.date()}&from={currency}&to=EUR"
        ) as response:
            data = await response.json()
            if response.status != 200:
                raise ExchangeException(f"Unable to get exchange rate for {currency}")

            rate = data["info"]["rate"]
            CURRENCY_RATE_CACHE[currency] = (rate, datetime.now() + config.EXPIRE_CACHE_TIME)
            return rate
