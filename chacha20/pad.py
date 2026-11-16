# Takes a message in text format as a string and outputs and array of assci code of each letter in the text.
# in the array it adds terminator character, '1', plus bytes of zero for making the length of the text divisble by 64

def padding(msg):
        zeros = (64 - ((len(msg) + 1) % 64)) % 64
        return msg + [0x80] + [0]*zeros


def unpadding(msg):
        i = 1
        while(msg[-i] != 0x80):
                i += 1
        return msg[:-i]
