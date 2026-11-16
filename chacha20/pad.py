#Padding makes a message length a multiple of the 64-byte ChaCha20 block.

def padding(msg):

        zeros = (64 - ((len(msg) + 1) % 64)) % 64
        return msg + [0x80] + [0]*zeros


def unpadding(msg):
        #Remove the padding added by padding(); returns None if the padding is invalid.
        i = len(msg) - 1
        while i >= 0 and msg[i] == 0:
                i -= 1
        if i < 0 or msg[i] != 0x80 or len(msg) - i > 64:
                return None
        return msg[:i]
