from typing import List

import pytest

from src.field import GF2PolynomialField
from src.field import ZpField
from src.polynomial.polynomial import Polynomial


def test_zp_field_invert():
    field = ZpField(order=11)

    assert field.invert(3) == 4
    assert field.invert(12) == 1
    assert field.invert(24) == 6
    assert field.invert(-1) == 10
    assert field.invert(-50) == 9


def test_zp_field_modulus():
    field = ZpField(order=11)

    assert field.modulus(11) == 0
    assert field.modulus(12) == 1
    assert field.modulus(24) == 2
    assert field.modulus(-1) == 10
    assert field.modulus(-56) == 10


@pytest.mark.parametrize(
    'polynomial_coef, invert_polynomial_coef',
    [
        ([0., 0., 0., 1.], [1., 1., 1., 1.]),
        ([1., 1., 0., 1.], [1., 0., 1.]),
        ([1.], [1.]),
    ],
)
def test_gf2_field_invert(polynomial_coef, invert_polynomial_coef):
    """
    Тест над полем с характеристикой 2 над многочленом x^4 + x + 1
    """
    def assert_invert(poly_1: Polynomial, poly_2: Polynomial):
        actual = field.invert(poly_1)
        actual = field.normalize_element(actual)

        assert poly_2 == actual

    field = GF2PolynomialField(Polynomial([1., 1., 0., 0., 1.]))

    polynomial = Polynomial(polynomial_coef)
    invert_polynomial = Polynomial(invert_polynomial_coef)

    assert_invert(polynomial, invert_polynomial)
    assert_invert(invert_polynomial, polynomial)


def test_gf2_field_modulus():
    """
    Тест над полем с характеристикой 2 над многочленом x^4 + x + 1
    """

    def modulus_polynomial(polynomial_coef: List[float]) -> Polynomial:
        polynomial = field.modulus(Polynomial(polynomial_coef))
        return field.normalize_element(polynomial)

    field = GF2PolynomialField(Polynomial([1., 1., 0., 0., 1.]))

    assert modulus_polynomial([.0, 1.]) == Polynomial([0., 1.])
    assert modulus_polynomial([0., 0., 0., 0., 1.]) == Polynomial([1., 1.])
    assert modulus_polynomial([*([0.] * 12), 1.]) == Polynomial([1., 1., 1., 1.])
    assert modulus_polynomial([*([0.] * 15), 1.]) == Polynomial([1.])
