from sage.all import Matrix, gcd
from string import ascii_uppercase


class ReccurentHillCipher:
    def __init__(
        self,
        key_matrix_1: Matrix,
        key_matrix_2: Matrix,
        alphabet: str = ascii_uppercase,
    ) -> None:
        self.pad_element = "A"
        self.alphabet = alphabet
        self.m = len(self.alphabet)
        if key_matrix_1.det() == 0 or key_matrix_2.det() == 0:
            raise Exception(f"det(Key Matrix) must not be equal to 0")
        if gcd(key_matrix_1.det(), self.m) != 1 or gcd(key_matrix_2.det(), self.m) != 1:
            raise Exception(f"GCD(Key, M) must be equal to 1")
        if (
            key_matrix_1.nrows() != key_matrix_1.ncols()
            or key_matrix_2.nrows() != key_matrix_2.ncols()
        ):
            raise Exception(f"Key matrix's numbers of columns and rows must be equal")
        if key_matrix_1.dimensions() != key_matrix_2.dimensions():
            raise Exception(f"Key matrix 1 and key matrix 2 not equal size")

        self.key_1, self.key_2 = key_matrix_1, key_matrix_2
        self.block_size = key_matrix_1.nrows()

    def _pad(self, text: str):
        return text + self.pad_element * (len(text) % self.block_size)

    def _unpad(self, text: str):
        return text.rstrip(self.pad_element)

    def get_key(self, block_number: int) -> Matrix:
        keys = [self.key_1, self.key_2]

        for i in range(0, block_number):
            if i > 1:
                new_key = keys[i - 1] * keys[i - 2] % self.m
                keys.append(new_key)
                yield new_key
            else:
                yield keys[i]

    def encrypt(self, plaintext: str):
        x = [self.alphabet.index(i) for i in self._pad(plaintext)]
        ciphertext_list = []
        keys = self.get_key(block_number=len(x) // self.block_size)
        for i in range(0, len(x), self.block_size):
            key = next(keys)
            block = x[i : i + self.block_size]
            cipher_block = key * Matrix(block).transpose()
            ciphertext_list.extend(cipher_block.list())
            if i - self.block_size * i > 1:
                self.keys.append(self.keys[i - self.block_size * i - 1] * key)
        ciphertext = "".join([self.alphabet[i % self.m] for i in ciphertext_list])
        return ciphertext

    def decrypt(self, ciphertext: str):
        y = [self.alphabet.index(i) for i in ciphertext]
        plaintext_list = []
        keys = self.get_key(block_number=len(y) // self.block_size)
        for i in range(0, len(y), self.block_size):
            key = next(keys)
            block = y[i : i + self.block_size]
            cipher_block = key.inverse() * Matrix(block).transpose()
            plaintext_list.extend(cipher_block.list())
        plaintext = "".join([self.alphabet[i % self.m] for i in plaintext_list])
        return self._unpad(plaintext)


if __name__ == "__main__":
    n = int(input("Key matrix size >> "))
    key_matrices = []
    for j in range(2):
        key_matrix_nth = []
        print(f"Key matrix {j+1}")
        for i in range(n):
            row = list(
                map(
                    int,
                    input(
                        f"Insert {i+1} row of key matrix with ',' (ex. '8, 6')>> "
                    ).split(","),
                )
            )
            key_matrix_nth.append(row)
        key_matrices.append(key_matrix_nth)

    cipher = ReccurentHillCipher(Matrix(key_matrices[0]), Matrix(key_matrices[1]))
    option = input("Choose option (`encrypt|decrypt) >> ").strip()
    match option:
        case "encrypt":
            plaintext = input("Insert plaintext to encrypt >> ")
            print(cipher.encrypt(plaintext=plaintext))
        case "decrypt":
            ciphertext = input("Insert ciphertext to decrypt >> ")
            print(cipher.decrypt(ciphertext=ciphertext))
