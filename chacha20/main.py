import subprocess

from Crypto.Random import get_random_bytes
from readchar import readkey
import enc_dec
import read_write


def KeyGen():
        key = get_random_bytes(32)
        return [f"{k:02x}" for k in key]

def NonceGen():
        nonce = get_random_bytes(12)
        return [f"{n:02x}" for n in nonce]




if __name__ == "__main__":
        print("U are using ChaCha20");
        print("Press E for Encrypting, D for Decrypting, any other key for exiting:")
        requested = readkey()
        if requested.upper() == 'E':
                print("Enter the path of the file to be encrypted: ")
                file_path = input()
                print("Enter the path of the output file: ")
                output_path = input()
                print("Enter the file name where to save the key: ")
                key_path = input()
                key = KeyGen()
                nonce = NonceGen()
                cipher = enc_dec.chacha20_encrypt(key, 0, nonce, read_write.reading_msg(file_path))
                read_write.writing_key(key, key_path)
                read_write.writing_cipher(cipher, nonce,output_path)
        elif requested.upper() == 'D':
                print("Enter the path of the file to be decrypted: ")
                file_path = input()
                print("Enter the path of the key file: ")
                key_path = input()
                key = read_write.reading_key(key_path)
                nonce, cipher = read_write.reading_cipher(file_path)
                decrypted = enc_dec.chacha20_decrypt(key, 0, cipher, nonce)
                print("Enter the path of the output file")
                output_path = input()
                read_write.writing_msg(decrypted, output_path)
                subprocess.run(["xdg-open", output_path])  # Linux
        else:
                print("Exiting...")
                exit(0)