from typing import Generic
from typing import TypeVar

from src.elliptic.elliptic import Point
from src.runner import TaskConfig


T = TypeVar('T')


class TaskAndResultFormatter(Generic[T]):
    def __init__(self, int_base: int):
        self._int_base = int_base

    def format(self, task_config: TaskConfig, result_point: Point[T]) -> str:
        pass

    @staticmethod
    def _format_polynomial(polynomial: str):
        pass
