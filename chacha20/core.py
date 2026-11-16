def Rot32(v: int, n: int):
        """Rotate a 32-bit word left by n bits.

        Args:
            v: 32-bit unsigned integer to rotate.
            n: Number of bit positions to rotate (0 < n < 32).

        Returns:
            The rotated value, kept within 32 bits.
        """
        a = (v << n) & 0xFFFFFFFF
        b = v >> (32-n)
        return (a | b)

def Quarter_Round(a: int, b: int, c: int, d: int):
        """Apply the ChaCha20 quarter-round to four 32-bit words (RFC 8439, 2.1).

        Each step is an add-rotate-xor (ARX) operation; additions are mod 2^32.

        Args:
            a, b, c, d: 32-bit unsigned integers.

        Returns:
            Tuple (a, b, c, d) of the updated words.
        """
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
        """Run a quarter-round on four words of the state selected by index.

        Args:
            state: List of 16 32-bit words (the ChaCha20 state); modified in place.
            i1, i2, i3, i4: Indices of the words to feed into the quarter-round.

        Returns:
            The updated state list.
        """
        state[i1], state[i2], state[i3], state[i4] = Quarter_Round(state[i1], state[i2], state[i3], state[i4])
        return state

def inner_block(state):
        """Perform one ChaCha20 double round on the state.

        The first four quarter-rounds operate on the columns of the 4x4 state
        matrix, the last four on its diagonals. Ten double rounds give the
        20 rounds of ChaCha20.

        Args:
            state: List of 16 32-bit words; modified in place.

        Returns:
            The updated state list.
        """
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
        """Convert the state words into a flat list of bytes in little-endian order.

        Args:
            state: List of 32-bit words.

        Returns:
            List of integers (0-255), four bytes per word, least significant first.
        """
        octats = []
        for word in state:
                for j in range(4):
                        octats.append(word%256)
                        word //= 256
        return octats

def mod2to32(state, initial_state):
        """Add the initial state to the working state word by word, mod 2^32.

        This is the final step of the ChaCha20 block function.

        Args:
            state: Working state after the 20 rounds; modified in place.
            initial_state: State as it was before the rounds; same length as state.

        Returns:
            The updated state list.
        """
        assert len(state) == len(initial_state)
        for i in range(len(state)):
                state[i] = (state[i] + initial_state[i]) % (2**32)
        return state

def le_bytes2num(b, t, n): # b[t][n]
        """Pack a list of hex byte strings into little-endian integer words.

        Args:
            b: List of t*n byte values as two-digit hex strings, e.g. ["00", "1f"].
            t: Number of words to produce.
            n: Number of bytes per word.

        Returns:
            List of t integers, each built from n bytes with the first byte
            as the least significant.
        """
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
        """Build the initial 16-word ChaCha20 state.

        Layout: 4 constant words ("expand 32-byte k") | 8 key words |
        1 block-counter word | 3 nonce words.

        Args:
            key: 32-byte key as a list of hex byte strings.
            counter: Block counter (integer).
            nonce: 12-byte nonce as a list of hex byte strings.

        Returns:
            List of 16 32-bit words.
        """
        constant = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

        state = constant + le_bytes2num(key, 8, 4) + [counter] + le_bytes2num(nonce, 3, 4)

        return state

def chacha20_block(key, counter, nonce):
        """Generate one 64-byte ChaCha20 keystream block (RFC 8439, 2.3).

        Args:
            key: 32-byte key as a list of hex byte strings.
            counter: Block counter for this block.
            nonce: 12-byte nonce as a list of hex byte strings.

        Returns:
            List of 64 keystream bytes (integers 0-255).
        """

        state = key_setup(key, counter, nonce)  # constant | key | counter | nonce
        initial_state = state.copy()
        for i in range(10):
                state = inner_block(state)
        state = mod2to32(state, initial_state)
        return serialize(state)
