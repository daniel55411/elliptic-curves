import pytest

from src.elliptic.elliptic import Point
from src.output import FormattersRegistry
from src.output import IntFormatter
from src.output import PointFormatter
from src.output import PolynomialFormatter
from src.output import TaskConfigFormatter
from src.output import TaskResultFormatter
from src.polynomial.polynomial import Polynomial
from src.task import TaskConfig
from src.task import TaskResult
from src.task import TaskType


def test_int_formatter__bad_base():
    with pytest.raises(ValueError):
        IntFormatter(default_base=3)


def test_int_formatter():
    formatter = IntFormatter(default_base=8)

    assert formatter.format(20, {'base': 2}) == '0b10100'
    assert formatter.format(20, {'base': 8}) == '0o24'
    assert formatter.format(20, {'base': 10}) == '20'
    assert formatter.format(20, {'base': 16}) == '0x14'
    assert formatter.format(20, {}) == '0o24'


def test_polynomial_formatter(polynomial_formatter):
    polynomial = Polynomial([0., 0., 1., 0., 1.])
    assert polynomial_formatter.format(polynomial, {}) == '20'


def test_point_formatter(point_formatter):
    polynomial_point = Point(
        x=Polynomial([0., 0., 1.]),
        y=Polynomial([1., 1., 1.]),
    )
    assert point_formatter.format(polynomial_point, {}) == '(4, 7)'

    int_point = Point(x=14, y=27)
    assert point_formatter.format(int_point, {}) == '(14, 27)'


def test_task_config_formatter(task_config_formatter):
    task_config_add = TaskConfig(
        task_type=TaskType.ADD,
        points=(Point(1, 1), Point(3, 5)),
    )
    assert task_config_formatter.format(task_config_add, {}) == '(1, 1) + (3, 5)'

    task_config_mul = TaskConfig(
        task_type=TaskType.MUL,
        points=(Point(1, 2),),
        scalar=101,
    )
    assert task_config_formatter.format(task_config_mul, {}) == '101 * (1, 2)'


def test_task_result_formatter(task_result_formatter):
    task_result = TaskResult(
        task_config=TaskConfig(
            task_type=TaskType.ADD,
            points=(Point(1, 1), Point(3, 5)),
        ),
        result=Point(4, 6),
    )
    assert task_result_formatter.format(task_result, {}) == '(1, 1) + (3, 5) = (4, 6)'


@pytest.fixture
def int_formatter():
    return IntFormatter()


@pytest.fixture
def polynomial_formatter(int_formatter):
    return PolynomialFormatter(int_formatter)


@pytest.fixture
def registry(int_formatter, polynomial_formatter):
    registry = FormattersRegistry()
    registry.register(int_formatter)
    registry.register(polynomial_formatter)

    return registry


@pytest.fixture
def point_formatter(registry):
    return PointFormatter(registry)


@pytest.fixture
def task_config_formatter(int_formatter, point_formatter):
    return TaskConfigFormatter(point_formatter, int_formatter)


@pytest.fixture
def task_result_formatter(point_formatter, task_config_formatter):
    return TaskResultFormatter(task_config_formatter, point_formatter)
