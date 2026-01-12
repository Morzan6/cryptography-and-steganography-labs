class Polynomial:
    def __init__(self, coeffs: list[int], p: int = None):
        self.coeffs = [c % p if p else c for c in coeffs] if p else coeffs
        self.p = p
        while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
            self.coeffs.pop()

    def degree(self) -> int:
        return len(self.coeffs) - 1 if self.coeffs else -1

    def __add__(self, other: "Polynomial") -> "Polynomial":
        if self.p != other.p:
            raise ValueError("Многочлены должны быть над одним полем")
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            result.append((a + b) % self.p)
        return Polynomial(result, self.p)

    def __sub__(self, other: "Polynomial") -> "Polynomial":
        if self.p != other.p:
            raise ValueError("Многочлены должны быть над одним полем")
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = other.coeffs[i] if i < len(other.coeffs) else 0
            result.append((a - b) % self.p)
        return Polynomial(result, self.p)

    def __mul__(self, other: "Polynomial") -> "Polynomial":
        if self.p != other.p:
            raise ValueError("Многочлены должны быть над одним полем")
        result = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                result[i + j] = (result[i + j] + a * b) % self.p
        return Polynomial(result, self.p)

    def __mod__(self, other: "Polynomial") -> "Polynomial":
        if self.p != other.p:
            raise ValueError("Многочлены должны быть над одним полем")
        if other.degree() == -1:
            raise ValueError("Деление на ноль")
        remainder = Polynomial(self.coeffs[:], self.p)
        divisor_degree = other.degree()
        inverse_lead = pow(other.coeffs[-1], self.p - 2, self.p)
        while remainder.degree() >= divisor_degree:
            degree_diff = remainder.degree() - divisor_degree
            lead_coeff = remainder.coeffs[-1] * inverse_lead % self.p
            monomial = Polynomial([0] * degree_diff + [lead_coeff], self.p)
            remainder -= monomial * other
            while len(remainder.coeffs) > 1 and remainder.coeffs[-1] == 0:
                remainder.coeffs.pop()
        return remainder

    def __eq__(self, other: "Polynomial") -> bool:
        return self.coeffs == other.coeffs and self.p == other.p

    def __str__(self) -> str:
        if not self.coeffs:
            return "0"

        def fmt(index: int, coeff: int) -> str:
            if index == 0:
                return str(coeff)
            variable = "x" if index == 1 else f"x^{index}"
            return variable if coeff == 1 else f"{coeff}{variable}"

        terms = [fmt(i, c) for i, c in enumerate(self.coeffs) if c != 0]
        return " + ".join(reversed(terms)) if terms else "0"

class GFElement:
    def __init__(self, poly: Polynomial, field: "GaloisField"):
        self.poly = poly % field.poly_modulus
        self.field = field

    def __add__(self, other: "GFElement") -> "GFElement":
        if self.field != other.field:
            raise ValueError("Элементы должны быть в одном поле")
        return GFElement(self.poly + other.poly, self.field)

    def __sub__(self, other: "GFElement") -> "GFElement":
        if self.field != other.field:
            raise ValueError("Элементы должны быть в одном поле")
        return GFElement(self.poly - other.poly, self.field)

    def __mul__(self, other: "GFElement") -> "GFElement":
        if self.field != other.field:
            raise ValueError("Элементы должны быть в одном поле")
        return GFElement(self.poly * other.poly, self.field)

    def __pow__(self, exp: int) -> "GFElement":
        if exp < 0:
            raise ValueError("Отрицательные степени не поддерживаются")
        result = GFElement(Polynomial([1], self.field.p), self.field)
        base = self
        while exp > 0:
            if exp % 2 == 1:
                result *= base
            base *= base
            exp //= 2
        return result

    def __eq__(self, other: "GFElement") -> bool:
        return self.poly == other.poly and self.field == other.field

    def __str__(self) -> str:
        return str(self.poly)

    def __repr__(self) -> str:
        return str(self.poly)

    def inverse(self) -> "GFElement":
        if self == self.field.zero:
            raise ValueError("Нулевой элемент не имеет обратного")
        return self ** (self.field.order - 2)

    @property
    def inv(self) -> "GFElement":
        return self.inverse()

    def order(self) -> int:
        if self == self.field.zero:
            raise ValueError("Нулевой элемент не имеет мультипликативной степени")
        current = self.field.one
        for exp in range(1, self.field.order):
            current *= self
            if current == self.field.one:
                return exp
        return -1

class GaloisField:
    def __init__(self, p: int, n: int, poly_modulus: Polynomial):
        self.p = p
        if len(poly_modulus.coeffs) != n + 1:
            raise ValueError("Многочлен должен быть степени n")
        self.n = n
        self.order = p ** n
        self.poly_modulus = poly_modulus
        self.zero = GFElement(Polynomial([0], p), self)
        self.one = GFElement(Polynomial([1], p), self)
        self._log_tables: dict[tuple[int, ...], dict[tuple[int, ...], int]] = {}

    def element_from_coeffs(self, coeffs: list[int]) -> GFElement:
        return GFElement(Polynomial(coeffs, self.p), self)

    def _build_log_table(self, generator: GFElement) -> dict[tuple[int, ...], int]:
        key = tuple(generator.poly.coeffs)
        table: dict[tuple[int, ...], int] = {tuple(self.one.poly.coeffs): 0}
        current = self.one
        for exp in range(1, self.order):
            current *= generator
            coeffs_key = tuple(current.poly.coeffs)
            table[coeffs_key] = exp
            if current == self.one:
                if exp != self.order - 1:
                    raise ValueError("Генератор не образует мультипликативную группу поля")
                break
        self._log_tables[key] = table
        return table

    def _get_log_table(self, generator: GFElement) -> dict[tuple[int, ...], int]:
        key = tuple(generator.poly.coeffs)
        if key not in self._log_tables:
            return self._build_log_table(generator)
        return self._log_tables[key]

    def _coeffs_from_int(self, value: int) -> list[int]:
        coeffs = []
        temp = value
        for _ in range(self.n):
            coeffs.append(temp % self.p)
            temp //= self.p
        return coeffs

    def all_elements(self) -> list[GFElement]:
        elements = []
        for i in range(self.order):
            elements.append(self.element_from_coeffs(self._coeffs_from_int(i)))
        return elements

    def generators(self) -> list[GFElement]:
        gens = []
        for i in range(1, self.order):
            el = self.element_from_coeffs(self._coeffs_from_int(i))
            if el.order() == self.order - 1:
                gens.append(el)
        return gens

    def decompose(self, element: GFElement, generator: GFElement) -> int:
        if element == self.zero:
            raise ValueError("Нельзя разложить нулевой элемент")
        log_table = self._get_log_table(generator)
        key = tuple(element.poly.coeffs)
        if key not in log_table:
            raise ValueError("Элемент не в подгруппе, сгенерированной генератором")
        return log_table[key]

def main():
   p = 3
   n = 3
   poly_modulus = Polynomial([1, 0, 2, 1], p)
   print(poly_modulus)
   field = GaloisField(p, n, poly_modulus)
   print(field.poly_modulus)
   print(field.all_elements())
   print(field.generators())
#    print(GFElement(Polynomial([0,1],p),field))
#    print(GFElement(Polynomial([1,2],p))
   print(GFElement(Polynomial([0,0,1],p), field=field))
   power = field.decompose(GFElement(Polynomial([0,0,1],p), field=field), GFElement(Polynomial([0,1],p), field=field))
   print(power)
#    print(power)
#    assert field.all_elements()[2] == field.generators()[1] ** power
#    print(power)

if __name__ == "__main__":
    main()