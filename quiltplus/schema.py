# schemas.py
from dataclasses import make_dataclass

from fondat.data import make_datacls

K_OPT = "?"
K_DEF = "="


def parse(k, v):
    is_optional = k[0] == K_OPT
    has_default = K_DEF in v
    return (k, v)


def schema2class(name, fields):
    list = [parse(k, v) for k, v in fields.items()]
    return make_dataclass(name, list)
