from sage.all import Matrix, gcd
from string import ascii_uppercase


class HillCipher:
    def __init__(self, key_matrix: Matrix, alphabet: str = ascii_uppercase) -> None:
        self.pad_element = "A"
        self.alphabet = alphabet
        self.m = len(self.alphabet)
        if key_matrix.det() == 0:
            raise Exception(f"det(Key) must not be equal to 0")
        if gcd(key_matrix.det(), self.m) != 1:
            raise Exception(f"GCD(Key, M) must be equal to 1")
        if key_matrix.nrows() != key_matrix.ncols():
            raise Exception(f"Key matrix's numbers of columns and rows must be equal")
        self.key = key_matrix
        self.block_size = key_matrix.nrows()

    def _pad(self, text: str):
        return text + self.pad_element * (len(text) % self.block_size)

    def _unpad(self, text: str):
        return text.rstrip(self.pad_element)

    def encrypt(self, plaintext: str):
        x = [self.alphabet.index(i) for i in self._pad(plaintext)]
        ciphertext_list = []
        for i in range(0, len(x), self.block_size):
            block = x[i : i + self.block_size]
            cipher_block = self.key * Matrix(block).transpose()
            ciphertext_list.extend(cipher_block.list())
        ciphertext = "".join([self.alphabet[i % self.m] for i in ciphertext_list])
        return ciphertext

    def decrypt(self, ciphertext: str):
        y = [self.alphabet.index(i) for i in ciphertext]
        plaintext_list = []
        for i in range(0, len(y), self.block_size):
            block = y[i : i + self.block_size]
            cipher_block = self.key.inverse() * Matrix(block).transpose()
            plaintext_list.extend(cipher_block.list())
        plaintext = "".join([self.alphabet[i % self.m] for i in plaintext_list])
        return self._unpad(plaintext)


if __name__ == "__main__":
    n = int(input("Key matrix size >> "))
    key_matrix = []
    for i in range(n):
        row = list(
            map(
                int,
                input(f"Insert {i+1} row of key matrix with ',' (ex. '8, 6')>> ").split(
                    ","
                ),
            )
        )
        key_matrix.append(row)

    cipher = HillCipher(Matrix(key_matrix))
    option = input("Choose option (encrypt|decrypt) >> ").strip()
    match option:
        case "encrypt":
            plaintext = input("Insert plaintext to encrypt >> ")
            print(cipher.encrypt(plaintext=plaintext))
        case "decrypt":
            ciphertext = input("Insert ciphertext to decrypt >> ")
            print(cipher.decrypt(ciphertext=ciphertext))
