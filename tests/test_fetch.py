from datetime import datetime, timedelta
from typing import Dict, Tuple
import pytest

from exchangerateconversion.fetch import FetchExchangeRateWithCache


@pytest.fixture
def fetcher():
    return FetchExchangeRateWithCache()


@pytest.fixture
def cache_data() -> Dict[str, Tuple[float, datetime]]:
    return {
        "USD": (1.2345, datetime.now() + timedelta(minutes=30)),
        "JPY": (130.0, datetime.now() - timedelta(minutes=30)),
    }


@pytest.mark.asyncio
async def test_cached_rate(cache_data: Dict[str, Tuple[float, datetime]]) -> None:
    currency = "USD"
    date = datetime.now()
    fetcher = FetchExchangeRateWithCache(cache_data)
    rate = await fetcher.get_rate(currency, date)
    assert rate == cache_data[currency][0]


@pytest.mark.asyncio
async def test_expired_rate(fetcher) -> None:
    currency = "USD"
    date = datetime.now()
    fetcher.rates_cache[currency] = (1.2345, datetime.now() - timedelta(minutes=30))
    rate = await fetcher.get_rate(currency, date)
    assert rate != 1.2345
    assert fetcher.rates_cache[currency][0] != 1.2345


@pytest.mark.asyncio
async def test_uncached_rate(fetcher) -> None:
    currency = "USD"
    date = datetime.now()
    rate = await fetcher.get_rate(currency, date)
    assert rate != 1.2345
    assert fetcher.rates_cache[currency][0] != 1.2345


@pytest.mark.asyncio
async def test_get_rate(fetcher):
    # Test fetching a new currency and date
    rate = await fetcher.get_rate("USD", datetime(2022, 1, 1))
    assert isinstance(rate, float)

    # Test fetching the same currency and date again, should be cached
    rate = await fetcher.get_rate("USD", datetime(2022, 1, 1))
    assert isinstance(rate, float)

    # Test fetching an expired cached currency and date, should not be cached
    fetcher.rates_cache["USD"] = (1.0, datetime.now() - timedelta(hours=1))
    rate = await fetcher.get_rate("USD", datetime(2022, 1, 1))
    assert isinstance(rate, float)
    assert fetcher.rates_cache["USD"][0] == rate
