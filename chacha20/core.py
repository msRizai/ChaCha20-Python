def Rot32(v: int, n: int):
        #Rotate a 32-bit word left by n bits.
        a = (v << n) & 0xFFFFFFFF
        b = v >> (32-n)
        return (a | b)

def Quarter_Round(a: int, b: int, c: int, d: int):
        #Apply the ChaCha20 quarter-round to four 32-bit words (RFC 8439, 2.1).

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
        b = Rot32(b, 7)

        return a, b, c, d

def Qround(state, i1, i2, i3, i4):
        #Run a quarter-round on four words of the state selected by index.

        state[i1], state[i2], state[i3], state[i4] = Quarter_Round(state[i1], state[i2], state[i3], state[i4])
        return state

def inner_block(state):
        #Perform one ChaCha20 double round on the state.

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
        #Convert the state words into a flat list of bytes in little-endian order.

        octats = []
        for word in state:
                for j in range(4):
                        octats.append(word%256)
                        word //= 256
        return octats

def mod2to32(state, initial_state):
        #Add the initial state to the working state word by word, mod 2^32.

        assert len(state) == len(initial_state)
        for i in range(len(state)):
                state[i] = (state[i] + initial_state[i]) % (2**32)
        return state

def le_bytes2num(b, t, n): # b[t][n]
        #Pack a list of hex byte strings into little-endian integer words.

        words = []
        assert len(b) == t*n
        for i in range(t):
                piece = b[i*n : (i+1) * n]
                value = 0
                for j in range(n):
                        value = value + int(piece[j], 16) * (256**j) # Little-Indian 12 34 --> 34 12
                words.append(value)
        return words

def key_setup(key, counter, nonce):
        #Build the initial 16-word ChaCha20 state.

        constant = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

        state = constant + le_bytes2num(key, 8, 4) + [counter] + le_bytes2num(nonce, 3, 4)

        return state

def chacha20_block(key, counter, nonce):
        #Generate one 64-byte ChaCha20 keystream block (RFC 8439, 2.3).


        state = key_setup(key, counter, nonce)  # constant | key | counter | nonce
        initial_state = state.copy()
        for i in range(10):
                state = inner_block(state)
        state = mod2to32(state, initial_state)
        return serialize(state)
