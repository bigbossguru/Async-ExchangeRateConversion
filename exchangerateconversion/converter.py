from datetime import datetime

from .fetch_rate import get_exchange_rate


async def convert_stake(message: dict) -> dict:
    """
    Converts the stake in the given message to EUR according to the exchange rate.
    """
    currency = message["payload"]["currency"]
    date = datetime.fromisoformat(message["payload"]["date"])
    try:
        rate = await get_exchange_rate(currency, date)
        converted_stake = round(message["payload"]["stake"] * rate, 5)
        message["payload"]["stake"] = converted_stake
        message["payload"]["currency"] = "EUR"
        return message
    except Exception as e:
        message_type = "error"
        message_text = f"Unable to convert stake. Error: {str(e)}"
        return {"type": message_type, "id": message["id"], "message": message_text}
