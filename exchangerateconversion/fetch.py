from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp

from .config import config


@dataclass
class FetchExchangeRateWithCache:
    """
    Fetches and store to the cache an two hours data the exchange rate for the given currency and date from the API.
    """

    rates_cache: Dict[str, float] = field(default_factory=dict)
    last_fetch: Optional[datetime] = None

    async def get_rate(self, currency: str, date: datetime) -> Optional[float]:
        """
        Fetches the exchange rate date from the external API.
        """
        if self.last_fetch is not None and (datetime.now() == (self.last_fetch + config.EXPIRE_CACHE_TIME)):
            self.rates_cache.clear()

        if currency in self.rates_cache:
            return self.rates_cache[currency]

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.EXCHANGE_RATE_API}/convert?date={date.date()}&from={currency}&to=EUR"
            ) as response:
                data = await response.json()
                if response.status == 200:
                    rate = data["info"]["rate"]
                    self.rates_cache[currency] = rate
                    if not self.rates_cache:
                        self.last_fetch = datetime.now()
                    return rate
        return None
