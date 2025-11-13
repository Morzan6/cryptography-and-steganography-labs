import numpy as np
from PIL import Image
import bitarray

class Metrics:
    def __init__(self, input_image_path: str, output_image_path: str, text: str= ""):
        self.output_image_path = output_image_path
        self.input_image_path = input_image_path

        input_image: Image.Image = Image.open(input_image_path)
        output_image: Image.Image = Image.open(output_image_path)
        self.image1: np.ndarray = np.array(input_image)
        self.image2: np.ndarray = np.array(output_image)

        self.text = text

    def _MSE(self):
        return np.square(self.image1 - self.image2).mean()
    
    def _RMSE(self):
        return np.sqrt(self._MSE())
    
    def _PNSR(self):
        return 10 * (np.log10(255**2 / self._MSE()))

    def _SSIM(self):
        K1 = 0.01
        K2 = 0.03
        L = 255

        mu_test = np.mean(self.image1)
        mu_out = np.mean(self.image2)

        var_test = np.var(self.image1)
        var_out = np.var(self.image2)

        cov = np.sum((self.image1-mu_test)*(self.image2-mu_out)) / (self.image1.size - 1)

        numenator = (2*mu_test* mu_out + K1 * L**2) * (2 *cov+ K2 * L**2)
        denominator = (mu_test**2 +mu_out**2 +K1 * L**2) * (var_test +var_out + K2 * L**2)
        ssim = numenator / denominator

        return ssim
    
    def _EC(self):
        text = Qim().decode(self.output_image_path)
        return len(text) * 8 / (self.image1.size - 1)
    
    def _BER(self):
        text_extracted = Qim().decode(self.output_image_path)
        diff = 0
        for i in range(len(text_extracted)):
            diff += bin(ord(self.text[i])^ ord(text_extracted[i])).count('1')

        ber = diff/ (len(self.text)*8)
        return ber
    
    def _NCC(self):
        text_extracted = Qim().decode(self.output_image_path)

        ba_original = bitarray.bitarray()
        ba_original.frombytes(self.text.encode('utf-8'))

        ba_extracted = bitarray.bitarray()
        ba_extracted.frombytes(text_extracted.encode('utf-8'))

        min_len = min(len(ba_original), len(ba_extracted))
        W = np.array(ba_original[:min_len], dtype=np.float64)
        W_ext = np.array(ba_extracted[:min_len], dtype=np.float64)

        numerator = np.sum(W * W_ext)
        denominator = np.sqrt(np.sum(W ** 2)) * np.sqrt(np.sum(W_ext ** 2))

        if denominator == 0:
            return 0.0
        return numerator / denominator

    def print_metrics(self):
        print(f"[+] Metrics: ")
        print(f"[+] MSE: {self._MSE()}")
        print(f"[+] RMSE: {self._RMSE()}")
        print(f"[+] PNSR: {self._PNSR()}")
        print(f"[+] SSIM: {self._SSIM()}")
        print(f"[+] EC: {self._EC()}")
        print(f"[+] BER: {self._BER()}")
        print(f"[+] NCC: {self._NCC()}")

class Qim:
    def __init__(self, q: int = 120):
        self.q: int = q
        self.metrics: Metrics
    
    def _open_image(self, src: str) -> np.ndarray:
        img: Image.Image = Image.open(src)
        return np.array(img)
    
    def encode(self, src: str, msg: str, output_path: str = 'encoded_image.png') -> None:
        img_arr = self._open_image(src)
        msg += '\0'
        
        ba = bitarray.bitarray()
        ba.frombytes(msg.encode('utf-8'))
        msg_bit_len: int = len(ba) 
        print(f"Original message: {msg}")
        print(f"Message as binary: {ba}")
        
        counter: int = 0
        b_counter: int = 0
        for i in img_arr:
            for pixel in i:
                for idx, c in enumerate(pixel):
                    if counter < msg_bit_len:
                        pixel[idx] = self.q * (c // self.q) + self.q / 2 * ba[b_counter]
                    else:
                        break
                    counter += 1
                    b_counter += 1

        self._save_image(img_arr, output_path)
        print(f"[+] Encoded image saved to {output_path}")

        self.metrics = Metrics(input_image_path=src, output_image_path=output_path, text=msg)
        self.metrics.print_metrics()
    
    def decode(self, src: str) -> str:
        img_arr = self._open_image(src)
        
        bit_str: str = ""
        decoded_bytes: bytearray = bytearray()
        byte_accumulator: int = 0
        bit_count: int = 0
        
        for i in img_arr:
            for pixel in i:
                for c in pixel:
                    P0 = self.q * (c // self.q)
                    P1 = self.q * (c // self.q) + self.q / 2
                    if abs(c - P0) < abs(c - P1):
                        bit_str += "0"
                    else:
                        bit_str += "1"
                    
                    bit_count += 1
                    if bit_count == 8:
                        byte_accumulator = int(bit_str[-8:], 2)
                        decoded_bytes.append(byte_accumulator)
                        bit_count = 0

                        if decoded_bytes[-1] == 0:
                            return decoded_bytes[:-1].decode('utf-8', errors='ignore')

        return decoded_bytes.decode('utf-8', errors='ignore')

    def _save_image(self, encoded_array: np.ndarray, output_path: str = 'encoded_image.png') -> None:
        image: Image.Image = Image.fromarray(encoded_array, "RGB")
        image.save(output_path)


def main() -> None:
    qim = Qim()
    
    print("[+] Select mode: ")
    print("1. Encode message into an image")
    print("2. Decode message from an image")
    response: str = input("Enter 1/2: ")
    
    if response == "1":
        src: str = input("[+] Enter image path: ")
        msg: str = input("[+] Enter message to encode in the image: ")
        output_path: str = input("Enter output path for encoded image (default is 'encoded_image.png'): ") or 'encoded_image.png'
        
        qim.encode(src, msg, output_path)
    
    elif response == "2":
        src: str = input("[+] Enter encoded image path: ")
        
        decoded_msg: str = qim.decode(src)
        print("[+] Decoded message:", decoded_msg)
    else:
        print("[+] Invalid selection. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
