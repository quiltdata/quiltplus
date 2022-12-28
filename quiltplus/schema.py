from dataclasses import dataclass, field, make_dataclass
from pathlib import Path
from typing import Any, Generic, Literal, Optional, TypedDict, TypeVar, Union

import yaml

K_OPT = "?"
K_DEF = "="


def field_default(split):
    return field(default=eval(split[1]))


def parse_field(k, v):
    is_optional = k[0] == K_OPT
    s = v.split(K_DEF)
    t = eval(s[0])
    if is_optional:
        t = Optional[t]
        k = k[1:]
        if len(s) == 1:
            s.append("None")
    return (k, t, field_default(s)) if len(s) > 1 else (k, t)


def schema2class(name, fields):
    list = [parse_field(k, v) for k, v in fields.items()]
    return make_dataclass(name, list)


def load_schemas(filename):
    yaml_string = Path(filename).read_text()
    dict = yaml.safe_load(yaml_string)
    klasses = [schema2class(k, v) for k, v in dict.items()]
    return klasses
