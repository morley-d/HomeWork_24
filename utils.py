import re
from typing import Iterable
from exceptions import NotBoolConvertedType, NotIntConvertedType


def build_query(it: Iterable, cmd: str, value: str) -> Iterable:
    res = list(map(lambda v: v.strip(), it))
    if cmd == 'filter':
        res = list(filter(lambda v: value in v, res))
    elif cmd == 'sort':
        if value not in ["True", "False"]:
            raise NotBoolConvertedType
        res = sorted(res, reverse=value == "True")
    elif cmd == 'unique':
        res = list(set(res))
    elif cmd == 'regex':
        regex = re.compile(value)
        res = list(filter(lambda v: regex.search(v), res))
    try:
        if cmd == 'limit':
            res = list(res[:int(value)])
        if cmd == 'map':
            res = list(map(lambda v: v.split(' ')[int(value)], res))
    except ValueError:
        raise NotIntConvertedType
    return res
