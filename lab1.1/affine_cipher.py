from string import ascii_uppercase
from math import gcd


class AffineCipher:
    def __init__(self, a: int, b: int, alphabet: str = ascii_uppercase) -> None:
        self.alphabet = alphabet
        self.m = len(self.alphabet)
        if a % self.m != a:
            raise Exception(f'"a" value must be in ZZ modulo {self.m}')
        if gcd(a, self.m) != 1:
            raise Exception(
                f"GCD(a, m) must be equal to 1, but it equal to {gcd(a, self.m)}"
            )
        self.a = a
        if b % self.m != b:
            raise Exception(f'"b" value muct be in ZZ modulo {self.m}')
        self.b = b

    def encrypt(self, plaintext: str) -> str:
        ciphertext = ""
        for char in plaintext:
            if char in self.alphabet:
                x = self.alphabet.index(char)
                ciphertext += self.alphabet[(self.a * x + self.b) % self.m]
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        for char in ciphertext:
            if char in self.alphabet:
                y = self.alphabet.index(char)
                plaintext += self.alphabet[
                    (y - self.b) * pow(self.a, -1, self.m) % self.m
                ]
            else:
                plaintext += char
        return plaintext


cipher = AffineCipher(a=11, b=17)
print(cipher.decrypt(cipher.encrypt("HELLO")))
