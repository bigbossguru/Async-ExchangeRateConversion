import json
import logging
from datetime import datetime

from .converter import convert_stake
from .fetch import FetchExchangeRateWithCache


async def handle_message(
    message: dict,
    exchange_rate_cache: FetchExchangeRateWithCache,
    ws=None,
) -> str:
    currency = message["payload"]["currency"]
    date = datetime.fromisoformat(message["payload"]["date"])

    # Get currency rate from external API or cache
    exchange_rate = await exchange_rate_cache.get_rate(currency, date)
    if exchange_rate is None:
        error_message = {
            "type": "error",
            "id": message["id"],
            "message": f"Unable to convert stake. Error: No exchange rate found for {currency} to EUR",
        }
        error_message_str = json.dumps(error_message)
        logging.warning(f"Unable to convert stake. Error: No exchange rate found for {currency} to EUR")
        if ws:
            await ws.send(error_message_str)
        return error_message_str

    else:
        # Converts the stake in the given message to EUR according to the exchange rate
        message = convert_stake(message, exchange_rate)
        message_str = json.dumps(message)
        if ws:
            await ws.send(message_str)
        logging.info(f"Converted the stake and sent to the server: {message_str}")
        return message_str
