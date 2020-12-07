import pytest

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
