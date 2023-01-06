import pytest

from elliptic_curves.polynomial.polynomial import Polynomial


def test_polynomial__constructor():
    assert Polynomial(3).bits == 3
    assert Polynomial([1, 1]).bits == 3
    assert Polynomial([1., 1.]).bits == 3
    assert Polynomial([0., 1., 0., 1.]).bits == 10


def test_polynomial__equals():
    assert Polynomial(3) == Polynomial(3)
    assert Polynomial(3) != Polynomial(4)

    with pytest.raises(ValueError):
        assert Polynomial(3) == 3


def test_polynomial__add():
    p1 = Polynomial([0., 1., 1.])
    p2 = Polynomial([0., 0., 1., 1., 1.])

    assert p1 + p2 == Polynomial([0., 1., 0., 1., 1.])


def test_polynomial__sub():
    p1 = Polynomial([0., 1., 1.])
    p2 = Polynomial([0., 0., 1., 1., 1.])

    assert p1 - p2 == Polynomial([0., 1., 0., 1., 1.])


def test_polynomial__len():
    assert len(Polynomial([1., 1., 0., 1.])) == 4
    assert len(Polynomial([0., 0., 0., 0.])) == 0


def test_polynomial__mul():
    p1 = Polynomial([0., 1., 0., 1., 0., 1.])
    p2 = Polynomial([1., 0., 1., 0., 0., 1.])
    p3 = Polynomial([0., 1., 0., 0., 0., 0., 1., 1., 1., 0., 1.])

    assert p1 * p2 == p3


def test_polynomial__mod():
    p1 = Polynomial([0., 1., 0., 1., 0., 1.])
    p2 = Polynomial([1., 0., 1., 0., 0., 1.])
    p3 = Polynomial([1., 1., 1., 1.])

    assert p1 % p2 == p3


def test_polynomial__lshift():
    p1 = Polynomial([0., 1., 1., 0., 1.])
    p2 = Polynomial([0., 0., 0., 1., 1., 0., 1.])

    assert p1 << 2 == p2


def test_polynomial__rshift():
    p1 = Polynomial([0., 1., 1., 0., 1.])
    p2 = Polynomial([1., 0., 1.])

    assert p1 >> 2 == p2


def test_polynomial__floordiv():
    p1 = Polynomial([0., 1., 1., 0., 1.])
    p2 = Polynomial([1., 0., 1.])
    p3 = Polynomial([0., 0., 1.])

    assert p1 // p2 == p3
