from dataclasses import dataclass
from enum import Enum
from enum import auto
from typing import Generic, List, Optional, Iterable

from src.elliptic import Point, Curve


class TaskType(Enum):
    ADD = auto()
    MUL = auto()


@dataclass
class TaskConfig(Generic[T]):
    task_type: TaskType
    points: List[Point[T]]
    scalar: Optional[int]


@dataclass
class TaskRunnerConfig(Generic[T]):
    curve_cls:
    curve_args: List[Any]
    task_configs: List[TaskConfig[T]]

@dataclass
class TaskRunner:
    curve: Curve[T]

    def run(self, tasks: List[TaskConfig[T]]) -> Iterable[Point[T]]:
        for task in tasks:
            yield self._run_task(task)

    def _run_task(self, task: TaskConfig) -> Point[T]:
        if task.task_type is TaskType.ADD:
            return self.curve.add(task.points[0], task.points[1])
        elif task.task_type is TaskType.MUL:
            return self.curve.mul(task.points[0], task.scalar)
