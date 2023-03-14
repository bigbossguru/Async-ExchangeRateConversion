import pytest
from exchangerateconversion.converter import convert_stake


@pytest.fixture
def message():
    return {"payload": {"stake": 100, "currency": "USD"}}


def test_convert_stake_converts_stake_correctly(message):
    rate = 0.85
    converted_message = convert_stake(message, rate)

    assert converted_message["payload"]["stake"] == 85.0


def test_convert_stake_sets_currency_to_eur(message):
    rate = 0.85
    converted_message = convert_stake(message, rate)

    assert converted_message["payload"]["currency"] == "EUR"


def test_convert_stake_returns_new_message_object(message):
    rate = 0.85
    converted_message = convert_stake(message, rate)

    assert converted_message is not message


def test_convert_stake_converts_stake_with_zero_rate(message):
    rate = 0
    converted_message = convert_stake(message, rate)

    assert converted_message["payload"]["stake"] == 0.0


def test_convert_stake_does_not_modify_original_message(message):
    rate = 0.85
    convert_stake(message, rate)

    assert message["payload"]["stake"] == 100
    assert message["payload"]["currency"] == "USD"
