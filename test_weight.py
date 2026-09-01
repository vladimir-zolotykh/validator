#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import wraps
import pytest

ENABLE_TRACK = 1


def track(func):
    if not ENABLE_TRACK:
        return func
    name = func.__qualname__

    @wraps(func)
    def wrapper(*args, **kwargs):
        val = args[1]
        print(f"{name}({val})")
        res = func(*args, **kwargs)
        return res

    return wrapper


class Validator:
    def __init_subclass__(cls):
        if validate := getattr(cls, "validate", None):
            setattr(cls, "validate", validate)

    def __set_name__(self, owner, name):
        self.sys_name = f"sys_{name}"
        self.usr_name = f"usr_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.sys_name)

    def validate(self, value):
        pass

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.sys_name, value)


class Typed(Validator):
    def validate(self, val):
        if not isinstance(val, self.expected_type):
            raise TypeError(f"{val} must be of type {self.expected_type}")
        super().validate(val)


class Integer(Typed):
    expected_type = int

    def validate(self, val):
        super().validate(val)


class Unsigned(Validator):
    def validate(self, val):
        if val < 0:
            raise ValueError(f"{val} must be 0 or above")
        super().validate(val)


class UnsignedInteger(Integer, Unsigned):
    def validate(self, val):
        super().validate(val)


class Thing:
    weight = UnsignedInteger()


if __name__ == "__main__":
    t = Thing()
    t.weight = 178
    print(t.weight)


def test_weight():
    t = Thing()
    t.weight = 178
    assert t.weight == 178
    with pytest.raises(TypeError, match="tall must be of type <class 'int'>"):
        t.weight = "tall"
    with pytest.raises(TypeError, match="12.3 must be of type <class 'int'>"):
        t.weight = 12.3
    with pytest.raises(ValueError, match="-60 must be 0 or above"):
        t.weight = -60
