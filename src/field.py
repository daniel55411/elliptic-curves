from abc import ABCMeta
from abc import abstractmethod
from copy import deepcopy
from typing import Generic
from typing import TypeVar

from numpy.polynomial import Polynomial
from numpy.polynomial.polynomial import polyone
from numpy.polynomial.polynomial import polyzero


T = TypeVar('T')


class Field(Generic[T], metaclass=ABCMeta):
    def __init__(self, order: T):
        self._order = order

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

    @classmethod
    @abstractmethod
    def zero(cls) -> T:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def one(cls) -> T:
        raise NotImplementedError


class ZpField(Field[int]):
    @classmethod
    def zero(cls) -> int:
        return 0

    @classmethod
    def one(cls) -> int:
        return 1


class GF2PolynomialField(Field[Polynomial]):
    @classmethod
    def zero(cls) -> Polynomial:
        return Polynomial(polyzero)

    @classmethod
    def one(cls) -> Polynomial:
        return Polynomial(polyone)
