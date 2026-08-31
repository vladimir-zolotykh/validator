#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.sys_name = f"sys_{name}"
        self.usr_name = f"usr_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.sys_name)

    @abstractmethod
    def validate(self, value):
        pass

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.sys_name, value)


class Typed(Validator):
    def validate(self, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{value!r}: expected {self.expected_type!r}")


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class MaxSized(Validator):
    def __init__(self, size=8):
        if size < 1:
            raise TypeError(f"{size} must be 1 or above")
        self.size = size


class String(Typed):
    expected_type = str


class SizedString(String, MaxSized):
    def validate(self, value):
        super().validate(value)
        if len(value) < 1 or len(value) > self.size:
            raise ValueError(f"{value} must be of length {self.size} or less")


class Member(Validator):
    def __init__(self, *values):
        self.members = values

    def validate(self, value):
        if value not in self.members:
            raise ValueError(f"{value!r} must be one of {self.members}")


class Unsigned(Validator):
    def validate(self, value):
        if value < 0:
            raise ValueError(f"{value}: must be >0")


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    def validate(self, value):
        super().validate(value)
        super(Typed, self).validate(value)


class Component:
    name = SizedString(size=8)
    price = UnsignedFloat()
    shares = UnsignedInteger()
    color = Member("RED", "GREEN", "BLUE")


if __name__ == "__main__":
    component = Component()
    component.name = "Apple"
    component.price = 123.5
    component.shares = 193
    component.color = "RED"
    c = component
    print(c.name, c.price, c.shares, c.color)
