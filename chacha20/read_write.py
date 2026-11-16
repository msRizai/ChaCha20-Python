def writing_key(key, file):
        with open(file, "w") as sk:
                sk.write(":".join(key) + "\n")

def writing_cipher(cipher, nonce, file): # file e.g. "/home/user/cipher.txt"
        with open(file, "w") as f:
                f.write(":".join(nonce) + "\n")
                f.write(bytes(cipher).hex() + "\n")

def writing_msg(msg, file):
        with open(file, "w") as f:
                f.write("".join(chr(a) for a in msg))

def reading_key(file):
        with open(file, "r") as f:
                return f.readline().strip().split(":") # returns the key

def reading_cipher(file):
        with open(file, "r") as f:
                nonce = f.readline().strip().split(":")
                cipher = list(bytes.fromhex(f.readline().strip()))
                return nonce, cipher # returns the cipher with nonce for decrypting

def reading_msg(file):
        with open(file, "rb") as f:
                return list(f.read()) # returns a list

