import pytest

from elliptic_curves.parser.common import parse_int


@pytest.mark.parametrize(
    'number_raw, expected',
    [
        ['12', 12],
        ['0xac', 172],
        ['0b11', 3],
        ['0o17', 15],
    ],
)
def test_parse_int(number_raw, expected):
    assert parse_int(number_raw) == expected
