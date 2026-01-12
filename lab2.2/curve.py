import argparse
import math
import random
from typing import List, Optional, Self
from pprint import pprint


class EllipticCurve:
    def __init__(self, a: int, b: int, p: int):
        """
        Создает эллиптическую кривую в форме y^2 = x^3 + ax + b (mod p)

        """
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("The curve is singular, choose different a and b.")
        self.a = a
        self.b = b
        self.p = p
        self._points_cache: Optional[List["Point"]] = None
        self._order_cache: Optional[int] = None


    def is_point_on_curve(self, x, y) -> bool:
        if x == None and y == None:
            return True
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0


    def enumerate_points(self, limit: Optional[int] = None) -> List["Point"]:
        if limit is None and self._points_cache is not None:
            cached = self._points_cache.copy()
            return cached

        points: List[Point] = []
        for x in range(self.p):
            rhs = (x**3 + self.a * x + self.b) % self.p
            if rhs == 0:
                points.append(Point(self, x, 0))
            else:
                legendre = pow(rhs, (self.p - 1) // 2, self.p)
                if legendre == 1:
                    y = Point.mod_sqrt(rhs, self.p)
                    points.append(Point(self, x, y))
                    if y != 0:
                        points.append(Point(self, x, (-y) % self.p))
            if limit is not None and len(points) >= limit:
                break

        points.append(Point.infinity(self))

        if limit is None:
            self._points_cache = points.copy()

        return points

    def order(self, max_points_to_try=10) -> int:
        if self._order_cache is not None:
            return self._order_cache

        p = self.p
        h_min = p + 1 - 2 * math.isqrt(p)
        h_max = p + 1 + 2 * math.isqrt(p)

        current_lcm = 1

        for i in range(max_points_to_try):
            try:
                P = self.random_point()
                if P.is_infinity():
                    continue
            except ValueError:
                continue 

            M = P.order()

            if M == 0:
                continue

            current_lcm = _lcm(current_lcm, M)

            possible_orders = []
            for N in range(h_min, h_max + 1):
                if N % current_lcm == 0:
                    possible_orders.append(N)
            
            if len(possible_orders) == 1:
                self._order_cache = possible_orders[0]
                return self._order_cache

        raise RuntimeError(f"Не удалось однозначно определить порядок кривой после {max_points_to_try} попыток.")

    def random_point(self) -> "Point":
        while True:
            x = random.randint(0, self.p - 1)
            rhs = (x**3 + self.a * x + self.b) % self.p
            try:
                y = Point.mod_sqrt(rhs, self.p)
                return Point(self, x, y)
            except ValueError:
                continue

    def prime_order_subgroups(self) -> List[List["Point"]]:
        subgroups: List[List[Point]] = []
        seen_signatures = set()

        for point in self.enumerate_points():
            if point.is_infinity():
                continue

            ord_point = point.order()
            if not _is_prime(ord_point):
                continue

            subgroup = [k * point for k in range(ord_point)]
            signature = _subgroup_signature(subgroup)

            if signature in seen_signatures:
                continue

            seen_signatures.add(signature)
            subgroups.append(subgroup)

        return subgroups

    def __str__(self) -> str:
        return f"EllipticCurve(a={self.a}, b={self.b}, p={self.p})"


class Point:
    def __init__(self, curve: EllipticCurve, x: int, y: int):
        """
        Новая точка на эллиптической кривой

        """
        self.curve = curve
        self.x = x
        self.y = y
        self._order_cache: Optional[int] = None

        if not (self.x is None and self.y is None):
            if not curve.is_point_on_curve(x, y):
                raise ValueError("The point is not on the given curve.")

    def order(self) -> int:
        if self._order_cache is not None:
            return self._order_cache

        if self.is_infinity():
            self._order_cache = 1
            return 1

        bound = self.curve.p + 1 + 2 * math.isqrt(self.curve.p)
        m = math.isqrt(bound) + 1

        baby_steps = {Point.infinity(self.curve): 0}
        current = self
        for k in range(1, m):
            if current.is_infinity():
                self._order_cache = k
                return k
            baby_steps.setdefault(current, k)
            current += self

        m_multiple = m * self
        if m_multiple.is_infinity():
            self._order_cache = m
            return m

        giant = m_multiple
        for j in range(1, m + 2):
            candidate = -giant
            if candidate in baby_steps:
                k = baby_steps[candidate]
                order = j * m + k
                if order > 0:
                    self._order_cache = order
                    return order
            giant += m_multiple
            if giant.is_infinity():
                order = (j + 1) * m
                self._order_cache = order
                return order

        current = self
        n = 1
        while True:
            if current.is_infinity():
                self._order_cache = n
                return n
            current += self
            n += 1

    def compress(self) -> str:
        """
        Возращает строковое представление сжатой точки
        """
        bx = bytes.fromhex(hex(self.x)[2:].zfill(64))
        by = bytes.fromhex(hex(self.y)[2:].zfill(64))
        y = 2 + (by[-1] & 1)
        out = bytearray(len(bx) + 1)
        out[0] = y
        out[1:] = bx
        return out.hex()

    @classmethod
    def uncompress(self, curve: EllipticCurve, compressed: str) -> Self:
        """
        Конвертирует сжатую точку в объект Point, находя Y координату
        """
        compressed_bytes = bytes.fromhex(compressed)
        sign_y = compressed_bytes[0] - 2
        x = int.from_bytes(compressed_bytes[1:], byteorder="big")

        rhs = (x**3 + curve.a * x + curve.b) % curve.p

        if pow(rhs, (curve.p - 1) // 2, curve.p) != 1:
            raise ValueError("The point is not on the given curve.")

        y = Point.mod_sqrt(rhs, curve.p)

        if y % 2 != sign_y:
            y = curve.p - y

        return Point(curve, x, y)

    def __neg__(self):
        if self.x is None or self.y is None:
            return self
        return Point(self.curve, self.x, (-self.y) % self.curve.p)

    @classmethod
    def infinity(cls, curve: EllipticCurve) -> Self:
        return cls(curve, None, None)

    def is_infinity(self) -> bool:
        return self.x is None and self.y is None

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.curve == other.curve and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.curve.a, self.curve.b, self.curve.p, self.x, self.y))

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("The operand must be a Point.")

        if self.curve != other.curve:
            raise ValueError("Points must be on the same curve.")

        if self.x is None and self.y is None:
            return other
        if other.x is None and other.y is None:
            return self

        if self.x == other.x and self.y != other.y:
            # P + (-P) = O 
            return Point(self.curve, None, None)

        if self.x == other.x:
            slope = (3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, self.curve.p)
        else:
            slope = (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)

        slope %= self.curve.p

        x_r = (slope**2 - self.x - other.x) % self.curve.p
        y_r = (slope * (self.x - x_r) - self.y) % self.curve.p

        return Point(self.curve, x_r, y_r)

    def __rmul__(self, n: int):
        result = Point(self.curve, None, None)
        temp = self

        while n > 0:
            if n % 2 == 1:
                result += temp
            temp += temp
            n //= 2

        return result

    def __repr__(self) -> str:
        if self.x is None or self.y is None:
            return "Point() on infinity"
        return f"Point({self.x}, {self.y}) on {self.curve.__str__()}"

    @staticmethod
    def mod_sqrt(a: int, p: int):
        """
        Вычисляет квадратный корень по модулю p, используя алгоритм Тонелли-Шанкса.
        """
        if pow(a, (p - 1) // 2, p) != 1:
            raise ValueError(f"No square root exists for {a} modulo {p}")

        if p % 4 == 3:
            return pow(a, (p + 1) // 4, p)

        s, q = 0, p - 1
        while q % 2 == 0:
            s += 1
            q //= 2

        z = 2
        while pow(z, (p - 1) // 2, p) != p - 1:
            z += 1

        m, c, t, r = s, pow(z, q, p), pow(a, q, p), pow(a, (q + 1) // 2, p)

        while t != 0 and t != 1:
            t2 = t
            i = 0
            for i in range(1, m):
                t2 = pow(t2, 2, p)
                if t2 == 1:
                    break
            else:
                raise RuntimeError("Tonelli-Shanks failed to converge.")

            b = pow(c, 2 ** (m - i - 1), p)
            c = pow(b, 2, p)
            t = (t * c) % p
            r = (r * b) % p
            m = i

        return r


def _is_prime(n: int, iterations: int = 5) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for _ in range(iterations):
        a = random.randrange(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False

    return True


def _subgroup_signature(points: List[Point]):
    def key(point: Point):
        if point.is_infinity():
            return (0, 0, 0)
        return (1, point.x, point.y)

    ordered = sorted(points, key=key)
    return tuple(key(point) for point in ordered)


def _lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def main():
    curve = EllipticCurve(3, 6, 29)
    point = Point(curve, 26, 17)
    print(curve.order())
    print(curve)
    pprint(curve.enumerate_points())
    pprint(curve.prime_order_subgroups())
    print(point.order())

if __name__ == "__main__":
    main()