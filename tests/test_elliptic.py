import pytest

from elliptic_curves.elliptic.elliptic import (GF2NotSupersingularCurve,
                                               GF2SupersingularCurve, Point,
                                               ZpCurve)
from elliptic_curves.polynomial.polynomial import Polynomial, polyone, polyzero


def pone() -> Polynomial:
    return Polynomial(polyone)


def pzero() -> Polynomial:
    return Polynomial(polyzero)


@pytest.mark.parametrize(
    'first_point, second_point, result',
    [
        (Point(None, None), Point(1, 1), Point(1, 1)),
        (Point(1, 1), Point(None, None), Point(1, 1)),
        (Point(1, 1), Point(1, -1), Point.infinity()),
        (Point(1, 2), Point(2, 1), Point(1, 1)),
        (Point(1, 2), Point(1, 2), Point(2, 2)),
        (Point(1, 0), Point(2, 0), Point(0, 0)),
    ],
)
def test_zp_curve__add(zp_curve, first_point, second_point, result):
    assert zp_curve.add(first_point, second_point) == result


@pytest.mark.parametrize(
    'point, result',
    [
        (Point(None, None), True),
        (Point(1, 0), True),
        (Point(1, 1), False),
    ],
)
def test_zp_curve__point_on_curve(zp_curve: ZpCurve, point, result):
    assert zp_curve.is_on_curve(point) == result


def test_zp_curve__all_points(zp_curve: ZpCurve):
    assert list(zp_curve.all_points()) == [Point(0, 0), Point(1, 0), Point(2, 0), Point[int].infinity()]


def test_zp_curve__point_order():
    curve = ZpCurve(97, 2, 3)
    assert curve.point_order(Point(3, 6)) == 5


@pytest.mark.parametrize(
    'first_point, scalar, result',
    [
        (Point(None, None), 2, Point(None, None)),
        (Point(1, 2), 2, Point(2, 2)),
    ],
)
def test_zp_curve__mul(zp_curve, first_point, scalar, result):
    assert zp_curve.mul(first_point, scalar) == result


@pytest.mark.parametrize(
    'first_point, second_point, result',
    [
        (Point(None, None), Point(pone(), pone()), Point(pone(), pone())),
        (Point(pone(), pone()), Point(None, None), Point(pone(), pone())),
        (
            Point(Polynomial([0., 0., 1.]), Polynomial([0., 1.])),
            Point(Polynomial([0., 0., 1.]), Polynomial([0., 1., 1.])),
            Point.infinity(),
        ),
        (
            Point(Polynomial([0., 1., 1.]), pone()),
            Point(Polynomial([0., 1., 1.]), pone()),
            Point(pone(), Polynomial([1., 1., 1.])),
        ),
        (
            Point(pone(), Polynomial([0., 1., 1.])),
            Point(Polynomial([0., 1., 1.]), Polynomial([1., 1., 1.])),
            Point(Polynomial([1., 1., 1.]), Polynomial([0., 1., 1.])),
        ),
    ],
)
def test_gf2_not_supersingular_curve__add(
    gf2_not_supersingular_curve: GF2NotSupersingularCurve,
    first_point: Point,
    second_point: Point,
    result: Point,
):
    assert gf2_not_supersingular_curve.add(first_point, second_point) == result


@pytest.mark.parametrize(
    'point, scalar, result',
    [
        (
            Point(Polynomial([0., 0., 0., 1.]), Polynomial([0., 1.])),
            2,
            Point(Polynomial([0., 1., 1.]), Polynomial([1., 1., 1.])),
        ),
        (
            Point(Polynomial([0., 0., 0., 1.]), Polynomial([0., 1.])),
            14,
            Point(Polynomial([0., 1., 1.]), Polynomial([1.])),
        ),
    ],
)
def test_gf2_not_supersingular_curve__mul(
    gf2_not_supersingular_curve: GF2NotSupersingularCurve,
    point: Point,
    scalar: int,
    result: Point,
):
    assert gf2_not_supersingular_curve.mul(point, scalar) == result


@pytest.mark.skip
@pytest.mark.parametrize(
    'first_point, second_point, result',
    [
        (Point(None, None), Point(pone(), pone()), Point(pone(), pone())),
        (Point(pone(), pone()), Point(None, None), Point(pone(), pone())),
        (
            Point(Polynomial([0., 1., 1.]), Polynomial([0., 1., 1.])),
            Point(Polynomial([0., 1., 1.]), Polynomial([1., 1., 1.])),
            Point.infinity(),
        ),
        (
            Point(Polynomial([0., 1., 1.]), pone()),
            Point(Polynomial([0., 1., 1.]), pone()),
            Point(pzero(), Polynomial([1., 1., 1.])),
        ),
        (
            Point(pone(), Polynomial([0., 1., 1.])),
            Point(Polynomial([0., 1., 1.]), Polynomial([1., 1., 1.])),
            Point(Polynomial([1., 1., 1.]), pzero()),
        ),
    ],
)
def test_gf2_supersingular_curve__add(
    gf2_supersingular_curve: GF2SupersingularCurve,
    first_point: Point,
    second_point: Point,
    result: Point,
):
    assert gf2_supersingular_curve.add(first_point, second_point) == result


@pytest.mark.skip
@pytest.mark.parametrize(
    'point, scalar, result',
    [
        (
            Point(Polynomial([0., 1., 1.]), pone()),
            2,
            Point(pzero(), Polynomial([1., 1., 1.])),
        ),
    ],
)
def test_gf2_supersingular_curve__mul(
    gf2_supersingular_curve: GF2SupersingularCurve,
    point: Point,
    scalar: int,
    result: Point,
):
    assert gf2_supersingular_curve.mul(point, scalar) == result


@pytest.fixture
def zp_curve() -> ZpCurve:
    return ZpCurve(3, -1, 3)


@pytest.fixture
def gf2_not_supersingular_curve():
    return GF2NotSupersingularCurve(
        p=Polynomial([1., 1., 0., 0., 1.]),
        a=pone(),
        b=pone(),
        c=pone(),
    )


@pytest.fixture
def gf2_supersingular_curve():
    return GF2SupersingularCurve(
        p=Polynomial([1., 1., 0., 0., 1.]),
        a=pone(),
        b=pone(),
        c=pone(),
    )
