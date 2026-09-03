#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class SymbolMeta(type):
    _symbols = {}

    def __call__(cls, name, pat):
        if name not in SymbolMeta._symbols:
            SymbolMeta._symbols[name] = super().__call__(name, pat)
        return SymbolMeta._symbols[name]


class Symbol(metaclass=SymbolMeta):
    def __init__(self, name, pat=""):
        print(f"Initializing Symbol({name!r})")
        self.name = name
        self.pat = pat

    def __repr__(self):
        return f"Symbol({self.name!r}, {self.pat!r})"


if __name__ == "__main__":
    # name = Symbol("NAME", r"[A-Za-z_]\w*")
    num = Symbol("NUM", r"\d+")
    print(num)
    num2 = Symbol("NUM", r"\d+")
    assert num is num2
