#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest


class Symbol:
    _instances = {}

    def __new__(cls, name: str, pat: str = ""):
        # if name not in type(cls)._instances:
        if name not in Symbol._instances:
            sym = super().__new__(cls)
            sym.name = name
            sym.pat = pat
            Symbol._instances[name] = sym
        return Symbol._instances[name]

    def __init__(self, name: str, pat: str = ""):
        pass

    def __repr__(self):
        return f"Symbol({self.name}, {self.pat})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            # There is no two Symbols with name NAME and different PAT
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return NotImplemented

    @classmethod
    def materpat(cls) -> str:
        return "|".join(
            f"(?P<{name}>{sym.pat})" for name, sym in cls._instances.items()
        )


def test_symbol_eq():
    Symbol._instances.clear()
    name = Symbol("NAME", r"[A-Za-z_]\w+")
    num = Symbol("NUM", r"\d+")
    assert name == Symbol("NAME")
    assert name == "NAME"
    assert name != num


def test_masterpat():
    Symbol._instances.clear()
    Symbol("NAME", r"[A-Za-z_]\w+")
    Symbol("NUM", r"\d+")
    assert Symbol.materpat() == r"(?P<NAME>[A-Za-z_]\w+)|(?P<NUM>\d+)"


@pytest.mark.parametrize(
    "name, pat",
    [
        ("NAME", r"[A-Za-z_]\w+"),
        ("NUM", r"\d+"),
    ],
)
def test_symbol(name, pat):
    sym = Symbol(name, pat)
    assert str(sym) == f"Symbol({name}, {pat})"
    assert sym is Symbol(name)


if __name__ == "__main__":
    Symbol("NAME", r"[A-Za-z_]\w+")
    Symbol("NUM", r"\d+")
    NUM1 = Symbol("NUM")
    NUM2 = Symbol("NUM")
    print(NUM1)
    assert NUM1 is NUM2
