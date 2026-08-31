import pytest
from validate import Component


def test_name():
    c = Component()
    c.name = "Utopia"
    assert c.name == "Utopia"
    with pytest.raises(ValueError, match="abracadabra must be of length 8 or less"):
        c.name = "abracadabra"

    with pytest.raises(TypeError, match="18: expected <class 'str'>"):
        c.name = 18


def test_price():
    c = Component()
    c.price = 123.4
    assert c.price == 123.4
    with pytest.raises(TypeError, match="'too much': expected <class 'float'>"):
        c.price = "too much"
    with pytest.raises(ValueError, match="-10.0: must be >0"):
        c.price = -10.0


def test_shares():
    c = Component()
    c.shares = 193
    assert c.shares == 193
    with pytest.raises(TypeError, match="'cheap': expected <class 'int'>"):
        c.shares = "cheap"
    with pytest.raises(ValueError, match="-10: must be >0"):
        c.shares = -10
