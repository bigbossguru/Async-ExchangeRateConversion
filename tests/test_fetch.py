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
    fetcher.rates_cache[currency] = 1.2

    # Call the method and verify that the cached rate is returned
    assert await fetcher.get_rate(currency, date) == 1.2


@pytest.mark.asyncio
async def test_get_rate_returns_cached_result(fetcher):
    currency = "USD"
    date = datetime.now()
    rate = 1.23

    # Cache the rate
    fetcher.last_fetch = date
    fetcher.rates_cache[currency] = rate

    not_expired_date = date + timedelta(minutes=30)

    # Fetch the rate and ensure it's returned from the cache
    fetched_rate = await fetcher.get_rate(currency, not_expired_date)
    assert fetched_rate == rate
