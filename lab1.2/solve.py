from sage.all import *

R = GF(29)

a, b, c, d, e, f, g, h = var("a b c d e f g h")

eqs = [
    12 * a + 4 * b == 26,
    12 * c + 4 * d == 15,
    4 * e + 19 * f == 0,
    4 * g + 19 * h == 23,
    12 * (e * a + f * c) + 4 * (e * b + f * d) == 15,
    12 * (g * a + h * c) + 4 * (g * b + h * d) == 12,
    19 * (f * (e * a + f * c) + h * (e * b + f * d)) == 27,
    19 * (f * (g * a + h * c) + h * (g * b + h * d)) == 21,
]

sol = solve(eqs, a, b, c, d, e, f, g, h)
print(sol)
for s in sol[0]:
    print(f"{s.left()}={R(s.rhs())}")
