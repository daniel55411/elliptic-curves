import pytest
from numpy.polynomial import Polynomial

from src.polynomial.utils import get_int_from_polynomial
from src.polynomial.utils import get_polynomial_from_int


@pytest.mark.parametrize(
    'number, expected_coefficients',
    [
        [7, [1., 1., 1.]],
        [12, [0., 0., 1., 1.]],
    ],
)
def test_get_polynomial_from_int(number, expected_coefficients):
    assert list(get_polynomial_from_int(number).coef) == expected_coefficients


@pytest.mark.parametrize(
    'polynomial, expected',
    [
        (Polynomial([0., 0., 1.]), 4),
        (Polynomial([0., 1., 1.]), 6),
        (Polynomial([1., 0., 1.]), 5),
    ],
)
def test_get_int_from_polynomial(polynomial, expected):
    assert get_int_from_polynomial(polynomial) == expected
