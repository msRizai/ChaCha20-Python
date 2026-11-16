from core import chacha20_block
from chacha20 import pad

def chacha20_encrypt(key, counter, nonce, text):
        """Pad a message and encrypt it with ChaCha20.

        The padded message is split into 64-byte blocks, and each block is
        XORed with the keystream block for counter + block index.

        Args:
            key: 32-byte key as a list of hex byte strings.
            counter: Initial block counter.
            nonce: 12-byte nonce as a list of hex byte strings.
            text: Plaintext as a list of byte values (integers 0-255).

        Returns:
            Ciphertext as a list of byte values; its length is a multiple of 64.
        """
        padded_text = pad.padding(text)
        encrypted_text = []
        for i in range(len(padded_text) // 64):
                keyS = chacha20_block(key, counter+i, nonce)
                block = padded_text[i*64:(i+1)*64]
                encrypted_text.extend(b ^ k for b, k in zip(block, keyS))
        return encrypted_text

def chacha20_decrypt(key , counter, cipher, nonce):
        """Decrypt a ChaCha20 ciphertext and remove its padding.

        Each 64-byte block is XORed with the keystream block for
        counter + block index; the padding added by chacha20_encrypt is then
        stripped.

        Args:
            key: 32-byte key as a list of hex byte strings.
            counter: Initial block counter (must match the one used to encrypt).
            cipher: Ciphertext as a list of byte values.
            nonce: 12-byte nonce as a list of hex byte strings.

        Returns:
            Plaintext as a list of byte values.
        """
        decrypted = []
        for i in range(len(cipher) // 64):
                keyS = chacha20_block(key, counter+i, nonce)
                block = cipher[i*64:(i+1)*64]
                decrypted.extend(b ^ k for b, k in zip(block, keyS))
        return pad.unpadding(decrypted)  # an array of asccii values
