import pytest
from datetime import datetime
import json

from exchangerateconversion.fetch import FetchExchangeRateWithCache
from exchangerateconversion.handler_msg import handle_message


@pytest.fixture
def exchange_rate_cache():
    return FetchExchangeRateWithCache()


@pytest.mark.asyncio
async def test_fetch_exchange_rate_with_cache(exchange_rate_cache):
    currency = "USD"
    date = datetime(2022, 1, 1)
    exchange_rate = await exchange_rate_cache.get_rate(currency, date)
    assert exchange_rate is not None
    assert isinstance(exchange_rate, float)


@pytest.mark.asyncio
async def test_handle_message(exchange_rate_cache):
    message = {"type": "message", "payload": {"currency": "USD", "date": "2022-01-01", "stake": 100}, "id": "1234"}

    result = await handle_message(message, exchange_rate_cache)
    assert result is not None

    result_json = json.loads(result)
    assert result_json["type"] == "message"
    assert "EUR" == result_json["payload"]["currency"]
