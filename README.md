# ChaCha20-Python

A from-scratch, pure-Python implementation of the **ChaCha20** stream cipher as specified in [RFC 8439](https://datatracker.ietf.org/doc/html/rfc8439), with a small command-line tool for encrypting and decrypting files.

> ⚠️ **Educational project.** This code was written to learn how ChaCha20 works internally. It has not been audited, is not constant-time, and provides no message authentication (no Poly1305). Do not use it to protect real data — use a vetted library such as [`cryptography`](https://cryptography.io/) or [PyCryptodome](https://www.pycryptodome.org/) instead.

## Features

- Full ChaCha20 block function: quarter round, column/diagonal rounds, 20 rounds total, and little-endian serialization
- File encryption and decryption for any file type (text, images, PDFs, …)
- Random 256-bit key and 96-bit nonce generation
- Tests against the official RFC 8439 test vectors

## Project structure

```
ChaCha20-Python/
├── chacha20/
│   ├── core.py         # ChaCha20 primitives: rotation, quarter round, state setup, block function
│   ├── enc_dec.py      # Encryption / decryption over 64-byte keystream blocks
│   ├── pad.py          # Padding and unpadding of the message to a multiple of 64 bytes
│   ├── read_write.py   # Reading/writing messages, keys and ciphertext files
│   └── main.py         # Interactive command-line interface
├── tests/
│   └── test_chacha20.py
└── pyproject.toml
```

## How it works

### The ChaCha20 state

Every 64-byte keystream block is generated from a 4×4 matrix of 32-bit words:

```
cccccccc  cccccccc  cccccccc  cccccccc     c = constant "expand 32-byte k"
kkkkkkkk  kkkkkkkk  kkkkkkkk  kkkkkkkk     k = 256-bit key
kkkkkkkk  kkkkkkkk  kkkkkkkk  kkkkkkkk
bbbbbbbb  nnnnnnnn  nnnnnnnn  nnnnnnnn     b = 32-bit block counter, n = 96-bit nonce
```

The block function (`chacha20_block` in [`core.py`](chacha20/core.py)):

1. Builds the initial state from the constant, key, counter and nonce (`key_setup`).
2. Applies 10 iterations of `inner_block` — 4 column quarter rounds followed by 4 diagonal quarter rounds — for 20 rounds in total.
3. Adds the original state to the result word by word, modulo 2³².
4. Serializes the 16 words into 64 bytes in little-endian order.

### Encryption and decryption

1. The plaintext is padded (see below) to a multiple of 64 bytes.
2. For each 64-byte chunk `i`, a keystream block is generated with counter `counter + i`.
3. The chunk is XORed with the keystream.

Decryption is the same XOR operation, followed by removing the padding.

### Padding

ChaCha20 is a stream cipher and doesn't strictly need padding. This project pads anyway so that every block is exactly 64 bytes: a `0x80` byte is appended to the message, followed by as many `0x00` bytes as needed. During decryption, everything from the last `0x80` byte onward is removed.

## Requirements

- Python 3.8+
- [`pycryptodome`](https://pypi.org/project/pycryptodome/) — used only to generate secure random keys and nonces
- [`readchar`](https://pypi.org/project/readchar/) — single-key input in the CLI
- [`pytest`](https://pypi.org/project/pytest/) — for running the tests

## Installation

```bash
git clone https://github.com/msRizai/ChaCha20-Python.git
cd ChaCha20-Python

python3 -m venv .venv
source .venv/bin/activate

pip install pycryptodome readchar pytest
```

## Usage

Run the CLI from inside the `chacha20/` directory:

```bash
cd chacha20
python main.py
```

You'll be asked to press a key:

- **E** — encrypt a file
- **D** — decrypt a file
- **any other key** — exit

### Encrypting

```
U are using ChaCha20
Press E for Encrypting, D for Decrypting, any other key for exiting:
Enter the path of the file to be encrypted:
photo.jpg
Enter the path of the output file:
photo.enc
Enter the file name where to save the key:
photo.key
```

This produces two files:

- **Key file** (`photo.key`): the 32-byte key as colon-separated hex, e.g. `3f:a1:…:9c`
- **Ciphertext file** (`photo.enc`):
  - line 1 — the 12-byte nonce as colon-separated hex
  - line 2 — the ciphertext as one hex string

Keep the key file secret. Anyone who has it can decrypt the ciphertext.

### Decrypting

```
Press E for Encrypting, D for Decrypting, any other key for exiting:
Enter the path of the file to be decrypted:
photo.enc
Enter the path of the key file:
photo.key
Enter the path of the output file
photo_decrypted.jpg
```

The decrypted file is written to the output path and then opened with `xdg-open` (Linux only).

## Running the tests

From the project root:

```bash
pytest
```

The tests check `Quarter_Round`, `Qround` and `chacha20_block` against the test vectors in RFC 8439, sections 2.1.1, 2.2.1 and 2.3.2.

## References

- [RFC 8439 — ChaCha20 and Poly1305 for IETF Protocols](https://datatracker.ietf.org/doc/html/rfc8439)
- D. J. Bernstein, [*ChaCha, a variant of Salsa20*](https://cr.yp.to/chacha/chacha-20080128.pdf)
