from numpy.polynomial import Polynomial


def get_polynomial_from_int(number: int) -> Polynomial:
    bits = list(map(int, list('{0:0b}'.format(number))[::-1]))
    return Polynomial(bits)
