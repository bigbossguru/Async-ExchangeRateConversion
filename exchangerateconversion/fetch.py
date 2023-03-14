from typing import Dict, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp

from .config import config


@dataclass
class FetchExchangeRateWithCache:
    """
    Fetches and store to the cache an two hours data the exchange rate for the given currency and date from the API.
    """

    rates_cache: Dict[str, Tuple[float, datetime]] = field(default_factory=dict)

    async def get_rate(self, currency: str, date: datetime) -> Optional[float]:
        """
        Fetches the exchange rate date from the external API.
        """
        if currency in self.rates_cache:
            rate, expiration = self.rates_cache[currency]
            if datetime.now() < expiration:
                return rate

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.EXCHANGE_RATE_API}/convert?date={date.date()}&from={currency}&to=EUR"
            ) as response:
                data = await response.json()
                if response.status == 200:
                    rate = data["info"]["rate"]
                    self.rates_cache[currency] = (rate, datetime.now() + config.EXPIRE_CACHE_TIME)
                    return rate
        return None
