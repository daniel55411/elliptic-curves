from abc import ABCMeta
from abc import abstractmethod
from copy import deepcopy
from typing import Generic
from typing import List
from typing import Optional
from typing import TypeVar

from numpy.polynomial import Polynomial
from numpy.polynomial.polynomial import polyone
from numpy.polynomial.polynomial import polyzero


T = TypeVar('T')


class Field(Generic[T], metaclass=ABCMeta):
    def __init__(self, order: T, char: Optional[int] = None):
        self._order = order
        self._char = char

    def invert(self, element: T) -> T:
        s, prev_s = self.zero(), self.one()
        r, prev_r = self._order, deepcopy(element)

        while r != self.zero():
            quotient = prev_r // r

            prev_r, r = r, prev_r - quotient * r
            prev_s, s = s, prev_s - quotient * s

        return self.modulus(prev_s)

    def modulus(self, element: T) -> T:
        return element % self._order

    def normalize_element(self, element: T) -> T:
        pass

    @classmethod
    @abstractmethod
    def zero(cls) -> T:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def one(cls) -> T:
        raise NotImplementedError


class ZpField(Field[int]):
    def __init__(self, order: int):
        super().__init__(order, order)

    @classmethod
    def zero(cls) -> int:
        return 0

    @classmethod
    def one(cls) -> int:
        return 1


class GF2PolynomialField(Field[Polynomial]):
    def __init__(self, order: Polynomial):
        super().__init__(order, char=2)

    def normalize_element(self, element: Polynomial) -> Polynomial:
        new_coefficients = [coef % self._char for coef in element.coef]
        non_zero_coefficients = [abs(coef) for coef in new_coefficients if coef != 0]

        if len(non_zero_coefficients) == 0:
            return self.zero()

        min_coefficient = min([abs(coef) for coef in new_coefficients if coef != 0])

        if min_coefficient == 0:
            return self.zero()

        new_coefficients = [coef / min_coefficient for coef in new_coefficients]
        # Для отладки
        new_coefficients = [coef % self._char for coef in new_coefficients]

        self._trim_coefficients(new_coefficients)

        return Polynomial(new_coefficients)

    @classmethod
    def zero(cls) -> Polynomial:
        return Polynomial(polyzero)

    @classmethod
    def one(cls) -> Polynomial:
        return Polynomial(polyone)

    @staticmethod
    def _trim_coefficients(coefficients: List[float]) -> None:
        while coefficients[-1] == 0:
            coefficients.pop()
