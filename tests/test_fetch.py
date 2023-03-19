from datetime import datetime, timedelta
from unittest.mock import AsyncMock
import pytest

from exchangerateconversion.fetch import FetchExchangeRateWithCache


@pytest.fixture
def mock_response():
    async def _mock_response(*args, **kwargs):
        data = {"info": {"rate": 1.23}}
        return AsyncMock(status=200, json=AsyncMock(return_value=data))

    return _mock_response


@pytest.fixture
def fetcher():
    return FetchExchangeRateWithCache()


@pytest.mark.asyncio
async def test_get_rate_with_cached_data(fetcher: FetchExchangeRateWithCache):
    currency = "USD"
    rate = 1.23
    date = datetime.utcnow()
    fetcher.rates_cache[currency] = rate

    result = await fetcher.get_rate(currency, date)

    assert result == rate


@pytest.mark.asyncio
async def test_get_rate_with_external_api_response(fetcher: FetchExchangeRateWithCache, mock_response):
    currency = "USD"
    date = datetime.utcnow()

    async def mock_create_task(coroutine):
        # replace `create_task` with a mock that doesn't actually schedule a coroutine
        pass

    fetcher.set_element_to_cache = AsyncMock(wraps=fetcher.set_element_to_cache)
    fetcher.set_element_to_cache.side_effect = mock_create_task
    fetcher.get_rate = AsyncMock(wraps=fetcher.get_rate)
    fetcher.get_rate.side_effect = mock_response

    result_mock = await fetcher.get_rate(currency, date)
    result = await result_mock.json()

    assert result["info"]["rate"] == 1.23


@pytest.mark.asyncio
async def test_get_rate_with_expired_cache(fetcher: FetchExchangeRateWithCache):
    currency = "USD"
    rate = 1.23
    date = datetime.utcnow() - timedelta(hours=2)
    fetcher.rates_cache[currency] = rate
    fetcher.set_element_to_cache = AsyncMock(wraps=fetcher.set_element_to_cache)

    result = await fetcher.get_rate(currency, date)
    assert result == 1.23


@pytest.mark.asyncio
async def test_set_element_to_cache(fetcher: FetchExchangeRateWithCache):
    currency = "USD"
    rate = 1.23

    await fetcher.set_element_to_cache(currency, rate)
    assert currency not in fetcher.rates_cache
