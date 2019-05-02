# vim: fdm=manual

import math


class Interval(object):
    def __init__(self, inf, sup):
        self.inf = inf
        self.sup = sup

    def cast(self, it):
        if isinstance(it, int):
            return Interval(it, it)
        elif isinstance(it, float):
            return Interval(it, it)
        elif isinstance(it, Interval):
            return it
        else:
            raise TypeError("Cannot cast type to Interval: %s" % type(it))

    def __add__(self, other):
        other = self.cast(other)
        return Interval(self.inf + other.inf, self.sup + other.sup)

    def __radd__(self, other):
        other = self.cast(other)
        return other + self

    def __neg__(self):
        return Interval(-self.sup, -self.inf)

    def __sub__(self, other):
        other = self.cast(other)
        return Interval(self.inf - other.sup, self.sup - other.inf)

    def __rsub__(self, other):
        other = self.cast(other)
        return other - self

    def __mul__(self, other):
        other = self.cast(other)
        return Interval(min(self.inf*other.inf, self.inf*other.sup, self.sup*other.inf, self.sup*other.sup),
                        max(self.inf*other.inf, self.inf*other.sup, self.sup*other.inf, self.sup*other.sup))

    def __rmul__(self, other):
        other = self.cast(other)
        return other * self

    def __truediv__(self, other):
        other = self.cast(other)
        # return Interval(min(self.inf/other.inf, self.inf/other.sup, self.sup/other.inf, self.sup/other.sup),
        #                 max(self.inf/other.inf, self.inf/other.sup, self.sup/other.inf, self.sup/other.sup))
        return self * Interval(min(1/other.inf, 1/other.sup), max(1/other.inf, 1/other.sup))

    def __rtruediv__(self, other):
        other = self.cast(other)
        return other / self

    def __pow__(self, n):
        if n == 0:
            return Interval(1, 1)
        elif n == 1:
            return self
        else:
            return (self*self)**(n-1)

    def exp(self):
        return Interval(math.exp(self.inf), math.exp(self.sup))

    def __eq__(self, other):
        other = self.cast(other)
        return self.inf == other.inf and self.sup == other.sup

    def __lt__(self, other):
        other = self.cast(other)
        return self.sup < other.inf

    def __le__(self, other):
        other = self.cast(other)
        return self.inf <= other.sup

    def __gt__(self, other):
        other = self.cast(other)
        return self.inf > other.sup

    def __ge__(self, other):
        other = self.cast(other)
        return self.sup >= other.inf

    def __contains__(self, it):
        return self.inf <= it <= self.sup


def exp(it):
    if isinstance(it, Interval):
        return it.exp()
    else:
        return math.exp(it)
