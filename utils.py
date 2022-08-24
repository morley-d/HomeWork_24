import re
from typing import Iterable
from exceptions import NotBoolConvertedType, NotIntConvertedType


def build_query(it, cmd: str, value: str) -> Iterable:
    res = list(map(lambda v: v.strip(), it))
    if cmd == 'filter':
        res = filter(lambda v: value in v, res)
    elif cmd == 'sort':
        if value == "True":
            value = True
        elif value == "False":
            value = False
        else:
            raise NotBoolConvertedType
        res = sorted(res, reverse=value)
    elif cmd == 'unique':
        res = set(res)
    elif cmd == 'regex':
        regex = re.compile(value)
        res = filter(lambda v: regex.search(v), res)
    try:
        if cmd == 'limit':
            res = list(res[:int(value)])
        if cmd == 'map':
            res = map(lambda v: v.split(' ')[int(value)], res)
    except ValueError:
        raise NotIntConvertedType
    return res
