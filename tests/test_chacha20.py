from chacha20.core import Quarter_Round, Qround, chacha20_block
def test_QuarterRound():
	a = 0x11111111
	b = 0x01020304
	c = 0x9b8d6f43
	d = 0x01234567
	assert Quarter_Round(a, b, c, d) == (0xEA2A92F4, 0xCB1CF8CE, 0x4581472E, 0x5881C4BB)



def test_Qround():
	i1, i2, i3, i4 = 2, 7, 8, 13
	state = ["879531e0", "c5ecf37d", "516461b1", "c9a62f8a", "44c20ef3", "3390af7f", "d9fc690b", "2a5f714c", "53372767", "b00a5631", "974c541a", "359e9963", "5c971061", "3d631689", "2098d9d6", "91dbd320"]
	state = [int(m, 16) for m in state]

	state1 = Qround(state, i1, i2, i3, i4)
	state1 = [f"{m:08x}" for m in state1]
	asked = "879531e0 c5ecf37d bdb886dc c9a62f8a 44c20ef3 3390af7f d9fc690b cfacafd2 e46bea80 b00a5631 974c541a 359e9963 5c971061 ccc07c79 2098d9d6 91dbd320".split(' ')
	assert state1 == asked


def test_chacha20_block():
        test = "10 f1 e7 e4 d1 3b 59 15 50 0f dd 1f a3 20 71 c4 c7 d1 f4 c7 33 c0 68 03 04 22 aa 9a c3 d4 6c 4e d2 82 64 46 07 9f aa 09 14 c2 d7 05 d9 8b 02 a2 b5 12 9c d1 de 16 4e b9 cb d0 83 e8 a2 50 3c 4e".split(' ')
        key = "00:01:02:03:04:05:06:07:08:09:0a:0b:0c:0d:0e:0f:10:11:12:13:14:15:16:17:18:19:1a:1b:1c:1d:1e:1f".split(':')
        nonce = "00:00:00:09:00:00:00:4a:00:00:00:00".split(':')
        Block_count = 1
        assert [f"{m:02x}" for m in chacha20_block(key, Block_count, nonce)] == test


