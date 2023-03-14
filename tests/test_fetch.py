import pytest
from datetime import datetime, timedelta

from exchangerateconversion.fetch import FetchExchangeRateWithCache


@pytest.fixture
def fetcher():
    return FetchExchangeRateWithCache()


@pytest.mark.asyncio
async def test_get_rate_cached(fetcher):
    currency = "USD"
    date = datetime.now()

    # Add the currency and rate to the cache
    fetcher.rates_cache[currency] = (1.2, datetime.now() + timedelta(hours=1))

    # Call the method and verify that the cached rate is returned
    assert await fetcher.get_rate(currency, date) == 1.2


@pytest.mark.asyncio
async def test_get_rate_returns_cached_result(fetcher):
    currency = "USD"
    date = datetime(2023, 3, 14, 12, 0, 0)
    rate = 1.23

    # Cache the rate
    fetcher.rates_cache[currency] = (rate, datetime.now() + timedelta(hours=1))

    # Fetch the rate and ensure it's returned from the cache
    fetched_rate = await fetcher.get_rate(currency, date)
    assert fetched_rate == rate
