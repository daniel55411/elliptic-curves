class EllipticCurveError(Exception):
    pass


class InfinitePoint(EllipticCurveError):
    pass


class CalculationError(EllipticCurveError):
    pass

class IncorrectOrder(EllipticCurveError):
    pass

class NotOnCurve(EllipticCurveError):
    pass
