from string import ascii_uppercase
from math import gcd
from galois_field import GaloisField, GFElement, Polynomial


class AffineCipher:
    def __init__(self, a: GFElement, b: GFElement, field: GaloisField) -> None:
        self.field = field
        if a == field.zero:
            raise ValueError("a не может быть нулевым элементом поля")
        self.a = a
        self.b = b

    def _convert_text_to_field_elements(self, text: str) -> list[GFElement]:
        result = []
        bin_text = "".join(format(ord(char), '08b') for char in text)

        while len(bin_text) % self.field.n != 0:
            bin_text += "0"

        for i in range(0, len(bin_text), self.field.n):
            result.append(self.field.element_from_coeffs([int(char) for char in bin_text[i:i + self.field.n]]))
        # print(bin_text)
        # print(result)
        return result

    def _convert_field_elements_to_text(self, field_elements: list[GFElement]) -> str:
        bin_text = ""
        for field_element in field_elements:
            padded_coeffs = field_element.poly.coeffs + [0] * (self.field.n - len(field_element.poly.coeffs))
            bin_text += "".join(str(int(coeff)) for coeff in padded_coeffs)

        while len(bin_text) % 8 != 0:
            bin_text += "0"

        return "".join(chr(int(bin_text[i:i + 8], 2)) for i in range(0, len(bin_text), 8))

    def _convert_field_elements_to_binstr(self, field_elements: list[GFElement]) -> str:
        bin_text = ""
        for field_element in field_elements:
            padded_coeffs = field_element.poly.coeffs + [0] * (self.field.n - len(field_element.poly.coeffs))
            bin_text += "".join(str(int(coeff)) for coeff in padded_coeffs)
        return bin_text

    def _convert_binstr_to_field_elements(self, binstr: str) -> list[GFElement]:
        result = []
        for i in range(0, len(binstr), self.field.n):
            result.append(self.field.element_from_coeffs([int(char) for char in binstr[i:i + self.field.n]]))
        return result

    def encrypt(self, plaintext: str) -> str:
        field_elements = self._convert_text_to_field_elements(plaintext)
        ciphertext = []
        for x in field_elements:
            ciphertext.append(self.a * x + self.b)
        return self._convert_field_elements_to_binstr(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        field_elements = self._convert_binstr_to_field_elements(ciphertext)
        print(ciphertext)
        print(field_elements)
        decrypted_field_elements = []
        for y in field_elements:
            decrypted_field_elements.append((y - self.b) * self.a.inv)
        return self._convert_field_elements_to_text(decrypted_field_elements)

field = GaloisField(2, 4, Polynomial([1,0,0,1,1], 2))
# print(Polynomial([1,0,0,1,1], 2))
a = GFElement(Polynomial([1], 2), field)
print(a)
b = GFElement(Polynomial([1], 2), field)
print(b)
cipher = AffineCipher(a=a, b=b, field=field)
print(cipher.encrypt("HELLO"))
print(cipher.decrypt(cipher.encrypt("HELLO")))
