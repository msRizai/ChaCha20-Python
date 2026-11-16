from core import chacha20_block
import pad

def chacha20_encrypt(key, counter, nonce, text):
        padded_text = pad.padding(text)
        encrypted_text = []
        for i in range(len(padded_text) // 64):
                keyS = chacha20_block(key, counter+i, nonce)
                block = padded_text[i*64:(i+1)*64]
                encrypted_text.extend(b ^ k for b, k in zip(block, keyS))
        return encrypted_text

def chacha20_decrypt(key , counter, cipher, nonce):
        print("key = ")
        print(key)
        print("counter = ")
        print(counter)
        print("cipher = ")
        print(cipher)
        print("nonce = ")
        print(nonce)
        decrypted = []
        for i in range(len(cipher) // 64):
                keyS = chacha20_block(key, counter+i, nonce)
                block = cipher[i*64:(i+1)*64]
                decrypted.extend(b ^ k for b, k in zip(block, keyS))
        return pad.unpadding(decrypted)  # an array of asccii values
