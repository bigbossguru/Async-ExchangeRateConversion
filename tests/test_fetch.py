from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientSession

from exchangerateconversion.fetch_rate import get_exchange_rate, CURRENCY_RATE_CACHE


@pytest.fixture(autouse=True)
def clear_cache():
    # Clear the currency rate cache before each test
    CURRENCY_RATE_CACHE.clear()


@pytest.mark.asyncio
async def test_get_exchange_rate_returns_float():
    currency = "USD"
    date = datetime.now()
    rate = await get_exchange_rate(currency, date)
    assert isinstance(rate, float)


@pytest.mark.asyncio
async def test_get_exchange_rate_caches_currency_rate():
    currency = "USD"
    date = datetime.now()
    rate1 = await get_exchange_rate(currency, date)

    # Call the function again with the same currency and date
    rate2 = await get_exchange_rate(currency, date)

    assert rate1 == rate2


@pytest.mark.asyncio
async def test_get_exchange_rate_handles_api_error(mocker):
    currency = "USD"
    date = datetime.now()

    # Mock the ClientSession object to return a response with an error status
    response_mock = AsyncMock()
    response_mock.status = 500
    response_mock.json = AsyncMock(return_value={"error": "Internal server error"})
    session_mock = MagicMock(spec=ClientSession)
    session_mock.get = AsyncMock(return_value=response_mock)

    mocker.patch("exchangerateconversion.fetch_rate.aiohttp.ClientSession", return_value=session_mock)

    with pytest.raises(Exception):
        await get_exchange_rate(currency, date)
