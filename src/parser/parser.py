from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Iterator
from typing import List
from typing import Tuple
from typing import TypeVar

from src.parser.errors import ParserError
from src.polynomial.polynomial import get_polynomial_from_int
from src.polynomial.polynomial import parse_polynomial
from src.runner import FieldType
from src.runner import TaskConfig
from src.runner import TaskRunnerConfig
from src.runner import TaskType


T = TypeVar('T')


class ArgsProvider(metaclass=ABCMeta):
    @abstractmethod
    def provide(self, input_lines: Iterator[str]) -> List[Any]:
        raise NotImplementedError


class ZpFieldArgsProvider(ArgsProvider):
    def provide(self, input_lines: Iterator[str]) -> List[Any]:
        return [int(next(input_lines))]


class ZpCurveArgsProvider(ArgsProvider):
    def provide(self, input_lines: Iterator[str]) -> List[Any]:
        return [
            int(next(input_lines)),
            int(next(input_lines)),
        ]


class GF2FieldArgsProvider(ArgsProvider):
    def provide(self, input_lines: Iterator[str]) -> List[Any]:
        value = next(input_lines)

        if 'x' in value:
            return [parse_polynomial(value)]

        return [int(value)]


class GF2CurveArgsProvider(ArgsProvider):
    def provide(self, input_lines: Iterator[str]) -> List[Any]:
        return [
            get_polynomial_from_int(int(next(input_lines))),
            get_polynomial_from_int(int(next(input_lines))),
            get_polynomial_from_int(int(next(input_lines))),
            get_polynomial_from_int(int(next(input_lines))),
            get_polynomial_from_int(int(next(input_lines))),
        ]


@dataclass
class FieldConfigurator:
    field_type: FieldType
    field_args_provider: ArgsProvider
    curve_args_provider: ArgsProvider


FIELDS_CONFIGURATORS = {
    'Z_p': FieldConfigurator(
        field_type=FieldType.Z_p,
        field_args_provider=ZpFieldArgsProvider(),
        curve_args_provider=ZpCurveArgsProvider(),
    ),
    'GF(2^m)': FieldConfigurator(
        field_type=FieldType.GF,
        field_args_provider=GF2FieldArgsProvider(),
        curve_args_provider=GF2CurveArgsProvider(),
    ),
}


TASKS_TYPES = {
    'a': TaskType.ADD,
    'm': TaskType.MUL,
}


class Parser:
    def parse(self, input_lines: Iterator[Tuple[int, str]]) -> TaskRunnerConfig:
        field_type = next(input_lines)

        if field_type not in FIELDS_CONFIGURATORS:
            raise ParserError('Неизвестное поле')

        configurator = FIELDS_CONFIGURATORS[field_type]
        field_args = configurator.field_args_provider.provide(input_lines)
        curve_args = configurator.curve_args_provider.provide(input_lines)

    def _parse_task(self, line: str) -> TaskConfig:
        line = line.lower()

        try:
            task_type = TASKS_TYPES[line]
        except KeyError:
            raise ParserError(f'Неизвестный тип операции: {line}')
