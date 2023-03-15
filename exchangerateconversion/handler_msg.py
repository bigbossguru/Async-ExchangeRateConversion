import json
import typing
import logging
from datetime import datetime

from .fetch import FetchExchangeRateWithCache
from .converter import convert_stake

exchange_rate_cache = FetchExchangeRateWithCache()


async def handle_message(message: dict) -> typing.Optional[str]:
    if message["type"] == "message":
        currency = message["payload"]["currency"]
        date = datetime.fromisoformat(message["payload"]["date"])

        # Get currency rate from external API or cache
        exchange_rate = await exchange_rate_cache.get_rate(currency, date)
        if exchange_rate is None:
            error_message = {
                "type": "error",
                "id": message["id"],
                "message": f"Unable to convert stake. Error: No exchange rate found for {currency} to EUR.",
            }
            return json.dumps(error_message)

        # Converts the stake in the given message to EUR according to the exchange rate
        message = convert_stake(message, exchange_rate)
        logging.info(f"Converted stake: {json.dumps(message)}")
        return json.dumps(message)
    return None
