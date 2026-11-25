import os


def is_hex_bytes(values, count):
        #Check that values is a list of count two-digit hex strings.
        if len(values) != count:
                return False
        try:
                return all(len(v) == 2 and 0 <= int(v, 16) <= 255 for v in values)
        except ValueError:
                return False

def writing_key(key, file):
        #Save a key to a text file as colon-separated hex bytes.
        with open(file, "w") as sk:
                sk.write(":".join(key) + "\n")

def writing_cipher(cipher, nonce, file): # file e.g. "/home/user/cipher.txt"
        #Save a nonce and ciphertext to a text file.
        with open(file, "w") as f:
                f.write(":".join(nonce) + "\n")
                f.write(bytes(cipher).hex() + "\n")

def writing_msg(msg, file):
        #Write a decrypted message to a file as raw bytes.
        with open(file, "wb") as f:
                f.write(bytes(msg))  # msg is a list of ascii values

def reading_key(file):
        #Read a key saved by writing_key().
        if not os.path.isfile(file):
                return None
        try:
                with open(file, "r") as f:
                        key = f.readline().strip().split(":")   # returns the key
        except (OSError, UnicodeDecodeError):
                return None
        if not is_hex_bytes(key, 32):
                return None
        return key

def reading_cipher(file):
        #Read a nonce and ciphertext saved by writing_cipher().
        if not os.path.isfile(file):
                return None, None
        try:
                with open(file, "r") as f:
                        nonce = f.readline().strip().split(":")
                        cipher = list(bytes.fromhex(f.readline().strip()))
        except (OSError, UnicodeDecodeError, ValueError):
                return None, None
        if not is_hex_bytes(nonce, 12) or len(cipher) == 0 or len(cipher) % 64 != 0:
                return None, None
        return nonce, cipher   # returns the cipher with nonce for decrypting

def reading_msg(file):
        #Read any file (text or binary) as raw bytes.
        if not os.path.isfile(file):
                return None
        try:
                with open(file, "rb") as f:
                        return list(f.read())  # returns a list
        except OSError:
                return None
