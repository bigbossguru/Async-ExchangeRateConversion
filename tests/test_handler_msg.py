import json
from datetime import datetime
import pytest

from exchangerateconversion.converter import convert_stake
from exchangerateconversion.handler_msg import handle_message


async def mock_get_rate(currency: str, date: datetime) -> float:
    # Mock implementation of the exchange rate API
    if currency == "USD":
        return 1.2
    if currency == "GBP":
        return 1.5
    return None


class MockFetchExchangeRateWithCache:
    """
    Mock class for featch exchange cache class
    """

    async def get_rate(self, currency: str, date: datetime) -> float:
        return await mock_get_rate(currency, date)


@pytest.fixture
def exchange_rate_cache():
    return MockFetchExchangeRateWithCache()


def test_convert_stake():
    message = {"id": 123, "payload": {"stake": 100, "currency": "USD", "date": "2022-01-01"}}
    rate = 1.2
    expected_output = {"id": 123, "payload": {"stake": 120, "currency": "EUR", "date": "2022-01-01"}}
    output = convert_stake(message, rate)
    assert output == expected_output


@pytest.mark.asyncio
async def test_handle_message(exchange_rate_cache):
    message = {"id": 123, "payload": {"stake": 100.0, "currency": "USD", "date": "2022-01-01"}}
    expected_output = {"id": 123, "payload": {"stake": 120.0, "currency": "EUR", "date": "2022-01-01"}}
    output = await handle_message(message, exchange_rate_cache)
    assert output == json.dumps(expected_output)

    # Test error case when exchange rate is not found
    message = {"id": 123, "payload": {"stake": 100, "currency": "JPY", "date": "2022-01-01"}}
    expected_output = {
        "type": "error",
        "id": 123,
        "message": "Unable to convert stake. Error: No exchange rate found for JPY to EUR",
    }
    output = await handle_message(message, exchange_rate_cache)
    assert output == json.dumps(expected_output)
