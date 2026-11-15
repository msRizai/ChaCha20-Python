import math

def Rot32(v: int, n: int):
        a = (v << n) & 0xFFFFFFFF
        b = v >> (32-n)
        return (a | b)
def Quarter_Round(a: int, b: int, c: int, d: int):
        a = (a+b) & 0xFFFFFFFF
        d = d^a
        d = Rot32(d, 16)

        c = (c+d) & 0xFFFFFFFF
        b = b ^ c
        b = Rot32(b, 12)

        a = (a+b) & 0xFFFFFFFF
        d = d^a
        d = Rot32(d, 8)

        c = (c+d) & 0xFFFFFFFF
        b = b^c
#       print(b)
        b = Rot32(b, 7)
#       print(b)

        return a, b, c, d



def Qround(state, i1, i2, i3, i4):
        state[i1], state[i2], state[i3], state[i4] = Quarter_Round(state[i1], state[i2], state[i3], state[i4])
        return state


def inner_block(state):
        state = Qround(state, 0, 4, 8, 12)
        state = Qround(state, 1, 5, 9, 13)
        state = Qround(state, 2, 6, 10, 14)
        state = Qround(state, 3, 7, 11, 15)
        state = Qround(state, 0, 5, 10, 15)
        state = Qround(state, 1, 6, 11, 12)
        state = Qround(state, 2, 7, 8, 13)
        state = Qround(state, 3, 4, 9, 14)
        return state



def serialize(state):
        octats = []
        for word in state:
                for j in range(4):
                        octats.append(word%256)
                        word //= 256
        return octats


def mod2to32(state, initial_state):
        assert len(state) == len(initial_state)
        for i in range(len(state)):
                state[i] = (state[i] + initial_state[i]) % (2**32)
        return state

# To complete




def le_bytes2num(b, t, n): # b[t][n]
        words = []
        print(f"the length of b is : {len(b)}")
        assert len(b) == t*n
        for i in range(t):
                piece = b[i*n : (i+1) * n]
                value = 0
                for j in range(n):
                        value = value + int(piece[j], 16) * (256**j) # Little-Indian 12 34 --> 34 12
                words.append(value)
        return words


def key_setup(key, counter, nonce):
        constant = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

        counter = int(f"{counter:08x}", 16)
        type(counter)
        state = constant + le_bytes2num(key, 8, 4) + [counter] + le_bytes2num(nonce, 3, 4)

        return state


def chacha20_block(key, counter, nonce):
        state = key_setup(key, counter, nonce)  # constant | key | counter | nonce
        initial_state = state.copy()
        print([f"{i:08x}" for i in state])

        for i in range(10):
                state = inner_block(state)
        print("\n After the 20 round mixing: \n")
        print([f"{i:08x}" for i in state])

        print("\n After the XoR and mod 2^32: \n")
        state = mod2to32(state, initial_state)
        print([f"{i:08x}" for i in state])

        return serialize(state)

def padding(plaintext: bytes) -> bytes:
    longueur_pad = 64 - (len(plaintext) % 64)
    if longueur_pad == 64:
        longueur_pad = 0
    return plaintext + b'\x00' * longueur_pad

def ChaCha20_encrypt(key, compteur, nonce, plaintext: bytes) -> bytes:
    plaintext_pad = padding(plaintext)
    nombre_blocs = len(plaintext_pad) // 64
    octets_chiffres = bytearray()
    
    compteur_courant = compteur
    for i in range(nombre_blocs):
        bloc_flux = bloc_chacha20(key, compteur_courant, nonce)
        bloc_clair = plaintext_pad[i * 64 : (i + 1) * 64]
        
        cyphertext = bytes(p ^ f for p, f in zip(bloc_clair, bloc_flux))
        octets_chiffres.extend(cyphertext)
        
        compteur_courant += 1
        
    return bytes(octets_chiffres)

def ChaCha20_decrypt(key, compteur, nonce, ciphertext: bytes) -> bytes:
    return ChaCha20_encrypt(key, counter, nonce, ciphertext)