from numpy.polynomial import Polynomial


def get_polynomial_from_int(number: int) -> Polynomial:
    bits = list(map(int, list('{0:0b}'.format(number))[::-1]))
    return Polynomial(bits)


def get_int_from_polynomial(polynomial: Polynomial) -> int:
    """
    NOTE: Рассчитывается, что полином над полем с характеристикой 2
    """
    bin_str = ''.join(map(lambda f: str(int(f)), polynomial.coef[::-1]))
    return int(bin_str, base=2)
