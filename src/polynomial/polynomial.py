import re

from numpy.polynomial import Polynomial

from src.polynomial.errors import PolynomialParseError
from src.polynomial.errors import UnknownIrreduciblePolynomialPower


__all__ = ['parse_polynomial', 'get_irreducible_polynomial', 'get_polynomial_from_int']


GF2_IRREDUCIBLE_POLYNOMIALS_DIRECTORY = {
    2: 'x^2+x+1,',
    3: 'x^3+x+1',
    4: 'x^4+x+1',
    5: 'x^5+x^2+1',
    6: 'x^6+x+1',
    7: 'x^7+x^3+1',
    8: 'x^8+x^4+x^3+x^2+1',
    9: 'x^9+x^4+1',
    10: 'x^10+x^3+1',
    11: 'x^11+x^2+1',
    12: 'x^12+x^6+x^4+x+1',
    13: 'x^13+x^4+x^3+x+1',
    14: 'x^14+x^10+x^6+x+1',
    15: 'x^15+x+1',
    16: 'x^16+x^12+x^3+x+1',
    17: 'x^17+x^3+1',
    18: 'x^18+x^7+1',
    19: 'x^19+x^5+x^2+x+1',
    20: 'x^20+x^3+1',
    21: 'x^21+x^2+1',
    22: 'x^22+x+1',
    23: 'x^23+x^5+1',
    24: 'x^24+x^7+x^2+x+1',
    25: 'x^25+x^3+1',
    26: 'x^26+x^6+x^2+x+1',
    27: 'x^27+x^5+x^2+x+1',
    28: 'x^28+x^3+1',
    29: 'x^29+x^2+1',
    30: 'x^30+x^23+x^2+x+1',
    31: 'x^31+x^3+1',
    32: 'x^32+x^22+x^2+x+1',
    36: 'x^36+x^11+1',
    40: 'x^40+x^9+x^3+x+1',
    48: 'x^48+x^28+x^3+x+1',
    56: 'x^56+x^42+x^2+x+1',
    64: 'x^64+x^46+x^4+x+1',
    72: 'x^72+x^62+x^3+x^2+1',
    80: 'x^80+x^54+x^2+x+1',
    96: 'x^96+x^31+x^4+x+1',
    128: 'x^128+x^7+x^2+x+1',
    160: 'x^160+x^19+x^4+x+1',
    192: 'x^192+x^107+x^4+x+1',
    256: 'x^256+x^16+x^3+x+1',
}


class _GF2IrreduciblePolynomialParser:
    MONOMIAL_PATTERN = re.compile(r'^(?:(\d+)\*?)?x\^(\d+)$')

    @classmethod
    def parse(cls, polynomial_raw: str) -> Polynomial:
        polynomial_raw = (
            polynomial_raw
            .replace(' ', '')
            .replace('-', '+')
            .strip(' +')
        )

        polynomial_powers = []
        for monomial_raw in polynomial_raw.split('+'):
            match = cls.MONOMIAL_PATTERN.match(monomial_raw)

            if match is None:
                raise PolynomialParseError(monomial_raw, polynomial_raw)

            scalar = int(match.group(1)) % 2
            power = int(match.group(2))

            if scalar != 0:
                polynomial_powers.append(power)

        polynomial_array = [0] * max(polynomial_powers)

        for power in polynomial_powers:
            polynomial_array[power] = 1

        return Polynomial(polynomial_array)


def parse_polynomial(polynomial: str) -> Polynomial:
    return _GF2IrreduciblePolynomialParser.parse(polynomial)


def get_irreducible_polynomial(power: int) -> Polynomial:
    if power not in GF2_IRREDUCIBLE_POLYNOMIALS_DIRECTORY:
        raise UnknownIrreduciblePolynomialPower(power)

    polynomial = GF2_IRREDUCIBLE_POLYNOMIALS_DIRECTORY[power]

    return _GF2IrreduciblePolynomialParser.parse(polynomial)


def get_polynomial_from_int(number: int) -> Polynomial:
    bits = list(map(int, list('{0:0b}'.format(number))))
    return Polynomial(bits)
