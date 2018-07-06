from dataclasses import dataclass
from typing import NewType

FlatId = NewType('FlatId', int)


@dataclass
class QueryUrl:
    url_base: str
    params: dict


@dataclass
class Flat:
    id: FlatId
    price: int
    url: str
