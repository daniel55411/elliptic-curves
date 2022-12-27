import pytest

from elliptic_curves.elliptic.elliptic import Point
from elliptic_curves.parser.input_stream import metrics
from elliptic_curves.parser.input_stream import Parser
from elliptic_curves.polynomial.polynomial import Polynomial
from elliptic_curves.task import FieldType
from elliptic_curves.task import TaskConfig
from elliptic_curves.task import TaskRunnerConfig
from elliptic_curves.task import TaskType


def test_parser__parse_zp_field():
    input_lines = [
        'Z_p',
        '  5',
        '3  ',
        ' 4 ',
        'a ( 1 , 2) (3, 4  )',
        'm (3, 4) 3',
        'm 2 (2, 1)',
    ]

    parser = Parser()
    actual = parser.parse(iter(input_lines))
    expected = TaskRunnerConfig(
        field_type=FieldType.Z_p,
        field_args=[5],
        curve_args=[3, 4],
        task_configs=[
            TaskConfig(
                task_type=TaskType.ADD,
                points=(Point(1, 2), Point(3, 4)),
            ),
            TaskConfig(
                task_type=TaskType.MUL,
                points=(Point(3, 4),),
                scalar=3,
            ),
            TaskConfig(
                task_type=TaskType.MUL,
                points=(Point(2, 1),),
                scalar=2,
            ),
        ],
    )
    assert actual == expected


@pytest.mark.parametrize(
    'irreducible_polynomial, expected_field_args',
    [
        ('x^2+x+1', [Polynomial([1., 1., 1.])]),
        ('m: 2', [2]),
    ],
)
def test_parser__parse_gf__irreducible_polynomial(irreducible_polynomial: str, expected_field_args: list):
    input_lines = [
        'GF(2^m)',
        irreducible_polynomial,
        '1',
        '2 ',
        ' 3',
        '   4',
        '5',
        'a ( 1 , 2) (3, 4  )',
        'm (3, 4) 3',
        'm 2 (2, 1)',
    ]

    parser = Parser()
    actual = parser.parse(iter(input_lines))
    expected = TaskRunnerConfig(
        field_type=FieldType.GF,
        field_args=expected_field_args,
        curve_args=[
            Polynomial([1.]),
            Polynomial([0., 1.]),
            Polynomial([1., 1.]),
            Polynomial([0., 0., 1.]),
            Polynomial([1., 0., 1.]),
        ],
        task_configs=[
            TaskConfig(
                task_type=TaskType.ADD,
                points=(
                    Point(Polynomial([1.]), Polynomial([0., 1.])),
                    Point(Polynomial([1., 1.]), Polynomial([0., 0., 1.])),
                ),
            ),
            TaskConfig(
                task_type=TaskType.MUL,
                points=(
                    Point(
                        Polynomial([1., 1.]),
                        Polynomial([0., 0., 1.]),
                    ),
                ),
                scalar=3,
            ),
            TaskConfig(
                task_type=TaskType.MUL,
                points=(
                    Point(
                        Polynomial([0., 1.]),
                        Polynomial([1.]),
                    ),
                ),
                scalar=2,
            ),
        ],
    )
    assert actual == expected


def test_parser__get_number_base_metric():
    input_lines = [
        'Z_p',
        '0x5',
        '0o3',
        '0b100 ',
        'a ( 0b1 , 0xAA) (3, 0x4  )',
    ]

    parser = Parser()
    actual = parser.parse(iter(input_lines))
    expected = TaskRunnerConfig(
        field_type=FieldType.Z_p,
        field_args=[5],
        curve_args=[3, 4],
        task_configs=[
            TaskConfig(
                task_type=TaskType.ADD,
                points=(Point(1, 170), Point(3, 4)),
            ),
        ],
    )

    assert actual == expected
    assert metrics.number_base == {
        2: 2,
        8: 1,
        10: 1,
        16: 3,
    }


@pytest.fixture(autouse=True)
def reset_metric():
    metrics.number_base.clear()
