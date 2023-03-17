from typing import Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import aiohttp
import logging
import asyncio

from .config import config


@dataclass
class FetchExchangeRateWithCache:
    """
    Fetches and store to the cache an two hours data the exchange rate for the given currency and date from the API.
    """

    rates_cache: Dict[str, float] = field(default_factory=dict)

    async def get_rate(self, currency: str, date: datetime) -> Optional[float]:
        """
        Fetches the exchange rate date from the external API.
        """
        if currency in self.rates_cache:
            logging.info("Get data from cache if exist")
            return self.rates_cache[currency]

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.EXCHANGE_RATE_API}/convert?date={date.date()}&from={currency}&to=EUR"
            ) as response:
                data = await response.json()
                if response.status == 200:
                    rate = data["info"]["rate"]
                    logging.info("Set cache incoming data from external API")
                    asyncio.create_task(self.set_element_to_cache(currency, rate))
                    return rate
        return None

    async def set_element_to_cache(self, currency, rate) -> None:
        self.rates_cache[currency] = rate
        await asyncio.sleep(config.EXPIRE_CACHE_TIME)
        logging.warning("Clear cache with the element of expiry time")
        del self.rates_cache[currency]
