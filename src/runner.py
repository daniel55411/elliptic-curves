from dataclasses import dataclass
from enum import auto
from enum import Enum
from typing import Generic
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from numpy.polynomial import Polynomial

from src.elliptic.elliptic import Curve
from src.elliptic.elliptic import GF2NotSupersingularCurve
from src.elliptic.elliptic import GF2SupersingularCurve
from src.elliptic.elliptic import Point
from src.elliptic.elliptic import ZpCurve
from src.polynomial.polynomial import get_irreducible_polynomial


T = TypeVar('T')


class TaskType(Enum):
    ADD = auto()
    MUL = auto()


class FieldType(Enum):
    Z_p = auto()
    GF = auto()


@dataclass
class TaskConfig(Generic[T]):
    task_type: TaskType
    points: Union[
        Tuple[Point[T], Point[T]],
        Tuple[Point[T]],
    ]
    scalar: Optional[int]


@dataclass
class TaskRunnerConfig(Generic[T]):
    field_type: FieldType
    field_args: List[Union[int, Polynomial]]
    curve_args: List[int]
    task_configs: List[TaskConfig[T]]

    def build_runner(self):
        curve = None

        if self.field_type is FieldType.Z_p:
            curve = ZpCurve(*self.field_args, *self.curve_args)
        elif self.field_type is FieldType.GF:
            p: Union[int, Polynomial] = self.field_args[0]

            if isinstance(p, int):
                p = get_irreducible_polynomial(power=p)

            try:
                a1, a2, a3, a4, a5 = self.curve_args
            except ValueError:
                raise ValueError('Неверное число коэффициентов эллиптической кривой')

            bool_args = list(map(lambda poly: bool(poly.coef), self.curve_args))
            if bool_args == [True, False, True, False, True]:
                curve = GF2NotSupersingularCurve(p, a1, a3, a5)
            elif bool_args == [False, True, False, True, True]:
                curve = GF2SupersingularCurve(p, a2, a4, a5)
            else:
                raise ValueError(
                    'Незивестная комбинация коэффициентов эллиптической'
                    ' кривой для конечного поля',
                )

        return TaskRunner(curve=curve)


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
