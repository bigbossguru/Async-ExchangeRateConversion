import json
from unittest.mock import patch

import pytest

from exchangerateconversion.handler_msg import handle_message


@pytest.mark.asyncio
async def test_handle_message():
    # Test case 1: message type is not "message"
    message = {"type": "other"}
    assert await handle_message(message) is None

    # Test case 2: exchange rate is not found in the cache
    message = {"type": "message", "id": 1, "payload": {"currency": "USD", "date": "2022-03-14", "stake": 100}}
    with patch("exchangerateconversion.handler_msg.exchange_rate_cache.get_rate") as mock_get_rate:
        mock_get_rate.return_value = None
        expected_result = {
            "type": "error",
            "id": 1,
            "message": "Unable to convert stake. Error: No exchange rate found for USD to EUR.",
        }
        assert json.loads(await handle_message(message)) == expected_result

    # Test case 3: stake is successfully converted to EUR
    message = {
        "type": "message",
        "id": 456,
        "payload": {
            "marketId": 123456,
            "selectionId": 987654,
            "odds": 2.2,
            "stake": 207.52054,
            "currency": "GBP",
            "date": "2021-05-18T21:32:42.324Z",
        },
    }
    exchange_rate = 1.15
    expected_result = {
        "type": "message",
        "id": 456,
        "payload": {
            "marketId": 123456,
            "selectionId": 987654,
            "odds": 2.2,
            "stake": 238.64862,
            "currency": "EUR",
            "date": "2021-05-18T21:32:42.324Z",
        },
    }
    with patch("exchangerateconversion.handler_msg.exchange_rate_cache.get_rate") as mock_get_rate:
        mock_get_rate.return_value = exchange_rate
        assert json.loads(await handle_message(message)) == expected_result
