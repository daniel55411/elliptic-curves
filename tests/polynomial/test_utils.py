import pytest

from src.polynomial.utils import convert_bits_array_to_num
from src.polynomial.utils import convert_num_to_bits_array


@pytest.mark.parametrize(
    'number, expected_coefficients',
    [
        [7, [1., 1., 1.]],
        [12, [0., 0., 1., 1.]],
    ],
)
def test_get_polynomial_from_int(number, expected_coefficients):
    assert list(convert_num_to_bits_array(number)) == expected_coefficients


@pytest.mark.parametrize(
    'coefficients, expected',
    [
        ([0., 0., 1.], 4),
        ([0., 1., 1.], 6),
        ([1., 0., 1.], 5),
    ],
)
def test_get_int_from_polynomial(coefficients, expected):
    assert convert_bits_array_to_num(coefficients) == expected
