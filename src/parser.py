from enum import Enum
from typing import Iterable
from typing import TypeVar

T = TypeVar('T')


class Fields(str, Enum):
    Zp = 'Z_p'
    GF = 'GF(m^2)'


class Parser:
    def parse(self, input_lines: Iterable[str]) -> :
