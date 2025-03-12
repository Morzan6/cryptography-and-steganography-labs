from string import ascii_uppercase
from enum import Enum
from typing import Generator


class VigenereMode(str, Enum):
    REPEATED_KEY = "REPEATED_KEY"
    PLAINTEXT_KEY = "PLAINTEXT_KEY"
    CIPHERTEXT_KEY = "CIPHERTEXT_KEY"


class VigenereCipher:
    def __init__(self, key: str, mode: VigenereMode):
        self.key = key
        self.alphabet = ascii_uppercase
        self.char_map = {char: i for i, char in enumerate(self.alphabet)}
        self.mode = mode

    def get_gamma(self) -> str:
        return {
            VigenereMode.REPEATED_KEY: self._repeated_gamma(),
            VigenereMode.PLAINTEXT_KEY: self._plaintext_gamma(),
            VigenereMode.CIPHERTEXT_KEY: self._ciphertext_gamma(),
        }.get(self.mode)

    def _repeated_gamma(self) -> Generator[str]:
        while True:
            for i in self.key:
                yield i

    def _plaintext_gamma(self) -> Generator[str]:
        for i in self.key:
            yield i
        i = 0
        while i < len(self.plaintext):
            yield self.plaintext[i]
            i += 1

    def _ciphertext_gamma(self) -> Generator[str]:
        for i in self.key:
            yield i
        i = 0
        while i < len(self.ciphertext):
            yield self.ciphertext[i]
            i += 1

    def encrypt(self, plaintext: str) -> str:
        self.plaintext = plaintext
        gamma = self.get_gamma()
        self.ciphertext = ""
        for i in range(len(plaintext)):
            if plaintext[i] in self.alphabet:
                encrypted = (
                    self.char_map[plaintext[i]] + self.char_map[next(gamma)]
                ) % len(self.alphabet)
                self.ciphertext += self.alphabet[encrypted]
            else:
                self.ciphertext += plaintext[i]
        return self.ciphertext

    def decrypt(self, ciphertext: str) -> str:
        self.ciphertext = ciphertext
        gamma = self.get_gamma()
        self.plaintext = ""
        for i in range(len(self.ciphertext)):
            if ciphertext[i] in self.alphabet:
                encrypted = (
                    self.char_map[ciphertext[i]] - self.char_map[next(gamma)]
                ) % len(self.alphabet)
                self.plaintext += self.alphabet[encrypted]
            else:
                self.plaintext += ciphertext[i]
        return self.plaintext


cipher = VigenereCipher(key="KEY", mode=VigenereMode.CIPHERTEXT_KEY)

print(cipher.decrypt(cipher.encrypt("HELLOWORLD")))
