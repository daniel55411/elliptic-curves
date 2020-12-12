import pytest

from src.parser.polynomial import parse_polynomial


@pytest.mark.parametrize(
    'polynomial_raw, expected_coefficients',
    [
        ('2 * x', [0.]),
        ('x', [0., 1.]),
        ('1', [1.]),
        ('0', [0.]),
        ('x^2', [0., 0., 1.]),
        ('- 3 * x^3 - 2 * x', [0., 0., 0., 1.]),
        ('  x^2 + x +   1  ', [1., 1., 1.]),
        ('x^4 + x + 1', [1., 1., 0., 0., 1.]),
    ],
)
def test_parse_polynomial(polynomial_raw, expected_coefficients):
    assert list(parse_polynomial(polynomial_raw).coef) == expected_coefficients
