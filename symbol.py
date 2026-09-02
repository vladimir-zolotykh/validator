#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Symbol:
    _instances = {}

    def __new__(cls, name: str, pat: str = ""):
        if name not in Symbol._instances:
            sym = super().__new__(cls)
            sym.name = name
            sym.pat = pat
            Symbol._instances[name] = sym
        return Symbol._instances[name]

    def __init__(self, name: str, pat: str = ""):
        pass

    def __repr__(self):
        return f"Symbol({self.name},{self.pat})"


if __name__ == "__main__":
    Symbol("NAME", r"[A-Za-z_]\w+")
    Symbol("NUM", r"\d+")
    NUM1 = Symbol("NUM")
    NUM2 = Symbol("NUM")
    print(NUM1)
    assert NUM1 is NUM2
