import numpy as np
from PIL import Image
import bitarray

class Qim:
    def __init__(self, q: int = 120):
        self.q: int = q 
    
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
