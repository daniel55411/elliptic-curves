import pytest

from src.elliptic.elliptic import Curve
from src.elliptic.elliptic import GF2NotSupersingularCurve
from src.elliptic.elliptic import GF2SupersingularCurve
from src.elliptic.elliptic import ZpCurve
from src.polynomial.polynomial import Polynomial
from src.polynomial.polynomial import polyone
from src.polynomial.polynomial import polyzero
from src.task import FieldType
from src.task import TaskRunnerConfig


NOT_SUPERSINGULAR_CURVE_ARGS = [
    Polynomial(polyone),
    Polynomial(polyzero),
    Polynomial(polyone),
    Polynomial(polyzero),
    Polynomial(polyone),
]


SUPERSINGULAR_CURVE_ARGS = [
    Polynomial(polyzero),
    Polynomial(polyone),
    Polynomial(polyzero),
    Polynomial(polyone),
    Polynomial(polyone),
]


def test_task_runner_config_build__zp_curve():
    config = TaskRunnerConfig(
        field_type=FieldType.Z_p,
        field_args=[5],
        curve_args=[3, 4],
        task_configs=[],
    )
    actual = config.build_runner()
    expected = ZpCurve(5, 3, 4)
    assert_curves_equals(actual.curve, expected)


@pytest.mark.parametrize('p', [2, Polynomial([1., 1., 1.])])
@pytest.mark.parametrize(
    'curve_args, expected_curve_cls',
    [
        (NOT_SUPERSINGULAR_CURVE_ARGS, GF2NotSupersingularCurve),
        (SUPERSINGULAR_CURVE_ARGS, GF2SupersingularCurve),
    ],
)
def test_task_runner_config_build__gf_curve(p, curve_args, expected_curve_cls):
    config = TaskRunnerConfig(
        field_type=FieldType.GF,
        field_args=[p],
        curve_args=curve_args,
        task_configs=[],
    )
    actual = config.build_runner()
    expected = expected_curve_cls(
        Polynomial([1., 1., 1.]),
        Polynomial(polyone),
        Polynomial(polyone),
        Polynomial(polyone),
    )
    assert_curves_equals(actual.curve, expected)


def test_task_runner_config_build__gf_curve__wrong_coef_count():
    config = TaskRunnerConfig(
        field_type=FieldType.GF,
        field_args=[2],
        curve_args=SUPERSINGULAR_CURVE_ARGS + NOT_SUPERSINGULAR_CURVE_ARGS,
        task_configs=[],
    )
    with pytest.raises(ValueError):
        config.build_runner()


def test_task_runner_config_build__gf_curve__unexpected_case():
    curve_args = SUPERSINGULAR_CURVE_ARGS.copy()
    curve_args[0] = Polynomial(polyone)
    config = TaskRunnerConfig(
        field_type=FieldType.GF,
        field_args=[2],
        curve_args=curve_args,
        task_configs=[],
    )
    with pytest.raises(ValueError):
        config.build_runner()


def assert_curves_equals(first_curve: Curve, second_curve: Curve):
    assert type(first_curve) == type(second_curve)
    assert_dict_equals(first_curve.__dict__, second_curve.__dict__)


def assert_dict_equals(first_dict: dict, second_dict: dict):
    assert len(first_dict) == len(second_dict)
    for key, value in first_dict.items():
        if isinstance(value, (int, str, Polynomial)):
            assert value == second_dict[key]
        else:
            assert_dict_equals(value.__dict__, second_dict[key].__dict__)
