import re
import os
import json
import pkg_resources
from functools import lru_cache
from typing import List, Union, Optional


__version__ = "0.0.2.post3"


RESOURCE_PATH: str = pkg_resources.resource_filename("demography", "data")


def _load_resource(origin: str, filename: str) -> str:
    path = os.path.join(RESOURCE_PATH, origin, filename)
    with open(path) as file:
        resource = file.read()
    return resource


@lru_cache(maxsize=128)
def _load_pattern(origin: str):
    return re.compile(_load_resource(origin, "regex"))


def validate_postcode(postcode: str, origin: str) -> str:
    if _load_pattern(origin).match(postcode) is None:
        raise ValueError(f"Postcode '{postcode}' is invalid.")
    return postcode


@lru_cache(maxsize=1)
def encoded_groups(origin: str):
    census = json.loads(_load_resource(origin, "groups.json"))
    return census


@lru_cache(maxsize=1)
def groups(origin: str) -> dict:
    encodings = json.loads(_load_resource(origin, "encodings.json"))
    inv_encodings = {v: k for k, v in encodings.items()}
    _encoded_groups = encoded_groups(origin)

    return {k: [inv_encodings[_] for _ in v] for k, v in _encoded_groups.items()}


@lru_cache(maxsize=1)
def oac_tree(origin: str) -> dict:
    return json.loads(_load_resource(origin, "tree.json"))


@lru_cache(maxsize=1)
def oac_map(origin: str) -> dict:
    return json.loads(_load_resource(origin, "map.json"))


def _get_parts(p: str) -> List[str]:
    parts = p.split(" ")
    if len(parts) == 1:
        return [parts[0], ""]
    else:
        return parts


def _get_oac(p: str, s: str, origin: str) -> str:
    region = oac_tree(origin)[p]
    code = region.get(s)
    if code is None:
        return oac_map(origin)[p]
    else:
        return code


def _get_groups(p: str, s: str, origin: str) -> List[str]:
    code = _get_oac(p, s, origin)
    return groups(origin)[code]


def _get_encoded_groups(p: str, s: str, origin: str) -> List[int]:
    code = _get_oac(p, s, origin)
    return encoded_groups(origin)[code]


@lru_cache(maxsize=1024)
def get(
    p: str,
    using: str = "oac",
    validate=False,
    origin: str = "uk",
    default: Optional[str] = None,
) -> Union[str, List[str], List[int], None]:
    p = validate_postcode(p, origin) if validate else p
    prefix, suffix = _get_parts(p)
    try:
        if using == "oac":
            return _get_oac(prefix, suffix, origin)
        elif using == "groups":
            return _get_groups(prefix, suffix, origin)
        elif using == "encoded_groups":
            return _get_encoded_groups(prefix, suffix, origin)
    except KeyError:
        return default
