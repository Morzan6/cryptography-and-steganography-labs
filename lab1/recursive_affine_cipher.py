from string import ascii_uppercase


class RecursiveAffineCipher:
    def __init__(
        self, k1: tuple[int, int], k2: tuple[int, int], alphabet: str = ascii_uppercase
    ):
        self.alphabet = alphabet
        self.m = len(self.alphabet)
        self.a1, self.b1 = k1
        self.a2, self.b2 = k2

    def encrypt(self, plaintext: str) -> str:
        ciphertext = ""
        a_list = [self.a1, self.a2]
        b_list = [self.b1, self.b2]
        for i in range(2, len(plaintext)):
            a_list.append(a_list[i - 1] * a_list[i - 2] % self.m)
            b_list.append(b_list[i - 1] + b_list[i - 2] % self.m)

        for i in range(len(plaintext)):
            if plaintext[i] in self.alphabet:
                a = a_list[i]
                b = b_list[i]
                x = self.alphabet.index(plaintext[i])
                ciphertext += self.alphabet[(a * x + b) % self.m]
            else:
                ciphertext += plaintext[i]
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        a_list = [self.a1, self.a2]
        b_list = [self.b1, self.b2]
        for i in range(2, len(ciphertext)):
            a_list.append(a_list[i - 1] * a_list[i - 2] % self.m)
            b_list.append(b_list[i - 1] + b_list[i - 2] % self.m)

        for i in range(len(ciphertext)):
            if ciphertext[i] in self.alphabet:
                y = self.alphabet.index(ciphertext[i])
                a = a_list[i]
                b = b_list[i]
                plaintext += self.alphabet[(y - b) * pow(a, -1, self.m) % self.m]
            else:
                plaintext += ciphertext[i]
        return plaintext


cipher = RecursiveAffineCipher(k1=(3, 5), k2=(5, 11))

print(cipher.decrypt(cipher.encrypt("HELLO")))
