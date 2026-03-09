from pathlib import Path

class GOST341112:
    def __init__(self, hash_size=512):
        assert hash_size in (256, 512), "Invalid hash size"
        self.hash_size = hash_size

        self.pi = self._get_pi_table()
        self.tau = self._get_tau_table()
        self.matrix_A = self._get_matrix_A()
        self.constants = self._get_constants()

    def _get_iv(self):
        if self.hash_size == 256:
            return (b'\x01' * 64)
        else:
            return bytes(64)

    def _get_pi_table(self):
        return [
            252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
            233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
            249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79,
            5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31,
            235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204,
            181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135,
            21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
            50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87,
            223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3,
            224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74,
            167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 173,
            69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88,
            179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 225, 27,
            131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97, 32, 113, 103,
            164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116, 210, 230,
            244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182
        ]

    def _get_tau_table(self):
        return [0, 8, 16, 24, 32, 40, 48, 56, 1, 9, 17, 25, 33, 41, 49, 57, 2, 10, 18, 26, 34, 42, 50, 58,
        3, 11, 19, 27, 35, 43, 51, 59, 4, 12, 20, 28, 36, 44, 52, 60, 5, 13, 21, 29, 37, 45, 53, 61, 6, 14,
        22, 30, 38, 46, 54, 62, 7, 15, 23, 31, 39, 47, 55, 63]

    def _get_matrix_A(self):
        matrix = []
        hex_rows = [
            "8e20faa72ba0b470", "47107ddd9b505a38", "ad08b0e0c3282d1c", "d8045870ef14980e",
            "6c022c38f90a4c07", "3601161cf205268d", "1b8e0b0e798c13c8", "83478b07b2468764",
            "a011d380818e8f40", "5086e740ce47c920", "2843fd2067adea10", "14aff010bdd87508",
            "0ad97808d06cb404", "05e23c0468365a02", "8c711e02341b2d01", "46b60f011a83988e",
            "90dab52a387ae76f", "486dd4151c3dfdb9", "24b86a840e90f0d2", "125c354207487869",
            "092e94218d243cba", "8a174a9ec8121e5d", "4585254f64090fa0", "accc9ca9328a8950",
            "9d4df05d5f661451", "c0a878a0a1330aa6", "60543c50de970553", "302a1e286fc58ca7",
            "18150f14b9ec46dd", "0c84890ad27623e0", "0642ca05693b9f70", "0321658cba93c138",
            "86275df09ce8aaa8", "439da0784e745554", "afc0503c273aa42a", "d960281e9d1d5215",
            "e230140fc0802984", "71180a8960409a42", "b60c05ca30204d21", "5b068c651810a89e",
            "456c34887a3805b9", "ac361a443d1c8cd2", "561b0d22900e4669", "2b838811480723ba",
            "9bcf4486248d9f5d", "c3e9224312c8c1a0", "effa11af0964ee50", "f97d86d98a327728",
            "e4fa2054a80b329c", "727d102a548b194e", "39b008152acb8227", "9258048415eb419d",
            "492c024284fbaec0", "aa16012142f35760", "550b8e9e21f7a530", "a48b474f9ef5dc18",
            "70a6a56e2440598e", "3853dc371220a247", "1ca76e95091051ad", "0edd37c48a08a6d8",
            "07e095624504536c", "8d70c431ac02a736", "c83862965601dd1b", "641c314b2b8ee083"
        ]
        matrix = []
        for row in hex_rows:
            matrix.append(bytes.fromhex(row))
        return matrix

    def _get_constants(self):
        return [
            bytes.fromhex( # C1
                "b1085bda1ecadae9ebcb2f81c0657c1f2f6a76432e45d016714eb88d7585c4fc"
                "4b7ce09192676901a2422a08a460d31505767436cc744d23dd806559f2a64507"
            ),
            bytes.fromhex( # C2
                "6fa3b58aa99d2f1a4fe39d460f70b5d7f3feea720a232b9861d55e0f16b50131"
                "9ab5176b12d699585cb561c2db0aa7ca55dda21bd7cbcd56e679047021b19bb7"
            ),
            bytes.fromhex( # C3
                "f574dcac2bce2fc70a39fc286a3d843506f15e5f529c1f8bf2ea7514b1297b7b"
                "d3e20fe490359eb1c1c93a376062db09c2b6f443867adb31991e96f50aba0ab2"
            ),
            bytes.fromhex( # C4
                "ef1fdfb3e81566d2f948e1a05d71e4dd488e857e335c3c7d9d721cad685e353f"
                "a9d72c82ed03d675d8b71333935203be3453eaa193e837f1220cbebc84e3d12e"
            ),
            bytes.fromhex( # C5
                "4bea6bacad4747999a3f410c6ca923637f151c1f1686104a359e35d7800fffbd"
                "bfcd1747253af5a3dfff00b723271a167a56a27ea9ea63f5601758fd7c6cfe57"
            ),
            bytes.fromhex( # C6
                "ae4faeae1d3ad3d96fa4c33b7a3039c02d66c4f95142a46c187f9ab49af08ec6"
                "cffaa6b71c9ab7b40af21f66c2bec6b6bf71c57236904f35fa68407a46647d6e"
            ),
            bytes.fromhex( # C7
                "f4c70e16eeaac5ec51ac86febf240954399ec6c7e6bf87c9d3473e33197a93c9"
                "0992abc52d822c3706476983284a05043517454ca23c4af38886564d3a14d493"
            ),
            bytes.fromhex( # C8
                "9b1f5b424d93c9a703e7aa020c6e41414eb7f8719c36de1e89b4443b4ddbc49a"
                "f4892bcb929b069069d18d2bd1a5c42f36acc2355951a8d9a47f0dd4bf02e71e"
            ),
            bytes.fromhex( # C9
                "378f5a541631229b944c9ad8ec165fde3a7d3a1b258942243cd955b7e00d0984"
                "800a440bdbb2ceb17b2b8a9aa6079c540e38dc92cb1f2a607261445183235adb"
            ),
            bytes.fromhex( # C10
                "abbedea680056f52382ae548b2e4f3f38941e71cff8a78db1fffe18a1b336103"
                "9fe76702af69334b7a1e6c303b7652f43698fad1153bb6c374b4c7fb98459ced"
            ),
            bytes.fromhex( # C11
                "7bcd9ed0efc889fb3002c6cd635afe94d8fa6bbbebab07612001802114846679"
                "8a1d71efea48b9caefbacd1d7d476e98dea2594ac06fd85d6bcaa4cd81f32d1b"
            ),
            bytes.fromhex( # C12
                "378ee767f11631bad21380b00449b17acda43c32bcdf1d77f82012d430219f9b"
                "5d80ef9d1891cc86e71da4aa88e12852faf417d5d9b21b9948bc924af11bd720"
            )
        ]

    def _S(self, data):
        return bytes([self.pi[b] for b in data])
    
    def _P(self, data):
        permuted = bytearray(64)
        for i in range(64):
            permuted[i] = data[self.tau[i]]
        return bytes(permuted)

    def _L(self, data):
        result = bytearray(64)
        for i in range(8):
            chunk = data[i*8:(i+1)*8]
            vec = int.from_bytes(chunk, byteorder='big')
            res = 0
            for j in range(64):
                if (vec >> (63-j)) & 1:
                    res ^= int.from_bytes(self.matrix_A[j], byteorder='big')
            result[i*8:(i+1)*8] = res.to_bytes(8, byteorder='big')
        return bytes(result)

    def _LPS(self, data):
        return self._L(self._P(self._S(data)))

    def _E(self, K, m):
        state = m
        Ks = [K]
        for i in range(1, 13):
            Ks.append(self._LPS(bytes(a ^ b for a, b in zip(Ks[i-1], self.constants[i-1]))))

        for i in range(12):
            state = self._LPS(bytes(a ^ b for a, b in zip(state, Ks[i])))
        return bytes(a ^ b for a, b in zip(state, Ks[-1]))

    def _g(self, N, h, m):
        K = self._LPS(bytes(a ^ b for a, b in zip(h, N)))
        return bytes(a ^ b ^ c for a, b, c in zip(self._E(K, m), h, m))

    def _pad(self, data):
        assert len(data) < 64, "Data block must be less than 64 bytes"
        padded = bytearray([0] * (64 - len(data) - 1))
        padded.append(0x01)
        padded.extend(data)
        assert len(padded) == 64
        return bytes(padded)

    def hash(self, data: bytes):
        h = self._get_iv()
        N = Sigma = bytes(64)
        
        first_block_size = len(data) % 64 or 64
        remaining_data = data[first_block_size:]
        
        for i in range(0, len(remaining_data), 64):
            block = remaining_data[i:i + 64]
            h = self._g(N, h, block)
            N = ((int.from_bytes(N, byteorder='big') + 512) % (2**512)).to_bytes(64, byteorder='big')
            Sigma = ((int.from_bytes(Sigma, byteorder='big') + int.from_bytes(block, byteorder='big')) % (2**512)).to_bytes(64, byteorder='big')
        
        first_block = data[:first_block_size]
        padded_block = first_block if len(first_block) == 64 else self._pad(first_block)
        h = self._g(N, h, padded_block)
        
        N = ((int.from_bytes(N, byteorder='big') + (512 if len(first_block) == 64 else len(first_block) * 8)) % (2**512)).to_bytes(64, byteorder='big')
        Sigma = ((int.from_bytes(Sigma, byteorder='big') + int.from_bytes(padded_block, byteorder='big')) % (2**512)).to_bytes(64, byteorder='big')
        
        return self._g(bytes(64), self._g(bytes(64), h, N), Sigma)[:(self.hash_size // 8)]
    
def main():
    hasher = GOST341112(hash_size=512)

   
    with open('test.txt', 'rb') as f:
        data = f.read()
        
    hash_value = hasher.hash(data).hex()

    hash_file = Path('test.txt').with_suffix('.hash')
    hash_file.write_text(hash_value)
    print(f"Хэш: {hash_value}")
            

if __name__ == "__main__":
    main()
