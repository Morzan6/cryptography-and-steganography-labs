from string import ascii_uppercase


class SimpleSubstitutionCipher:
    def __init__(self, key: str) -> None:
        self.key = key
        if len(self.key) != 26:
            raise Exception("Key length must be 26 symbols")
        if self.key.upper() != self.key:
            raise Exception("Key must be uppercase letters")
        self.alphabet = ascii_uppercase
        if set(self.key) != set(ascii_uppercase):
            raise Exception("Key must be latin letters")

        self.encryption_map = {k: v for k, v in zip(self.alphabet, self.key)}
        self.decryption_map = {k: v for k, v in zip(self.key, self.alphabet)}

    def encrypt(self, plaintext: str) -> str:
        ciphertext = ""
        for char in plaintext:
            if char in self.alphabet:
                ciphertext += self.encryption_map[char]
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        plaintext = ""
        for char in ciphertext:
            if char in self.alphabet:
                plaintext += self.decryption_map[char]
            else:
                plaintext += char
        return plaintext


cipher = SimpleSubstitutionCipher(key="QWERTYUIOPASDFGHJKLZXCVBNM")
print(cipher.decrypt(cipher.encrypt("HELLO")))
