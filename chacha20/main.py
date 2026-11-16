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




def __main__():
        print("U are using ChaCha20");
        print("Press E for Encrypting, D for Decrypting, any other key for exiting"
        requested = readkey()
        if requested.uppercase() == 'E':

