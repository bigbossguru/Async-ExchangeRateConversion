from copy import deepcopy


def convert_stake(message: dict, rate: float) -> dict:
    """
    Converts the stake in the given message to EUR according to the exchange rate.
    """
    message = deepcopy(message)
    converted_stake = round(message["payload"]["stake"] * rate, 5)
    message["payload"]["stake"] = converted_stake
    message["payload"]["currency"] = "EUR"
    return message
