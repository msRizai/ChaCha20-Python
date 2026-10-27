from chacha20.core import Quarter_Round, Qround
def test_QuarterRound():
	a = 0x11111111
	b = 0x01020304
	c = 0x9b8d6f43
	d = 0x01234567
	assert Quarter_Round(a, b, c, d) == (0xEA2A92F4, 0xCB1CF8CE, 0x4581472E, 0x5881C4BB)



def test_Qround():
	i1, i2, i3, i4 = 2, 7, 8, 13
	state = ["879531e0", "c5ecf37d", "516461b1", "c9a62f8a", "44c20ef3", "3390af7f", "d9fc690b", "2a5f714c", "53372767", "b00a5631", "974c541a", "359e9963", "5c971061", "3d631689", "2098d9d6", "91dbd320"]
	print("\nThe state after changes:\n")
	state1 = Qround(state, i1, i2, i3, i4)
	assert state1 == ["879531e0",  "c5ecf37d", "bdb886dc", "c9a62f8a", "44c20ef3", "3390af7f", "d9fc690b", "cfacafd2", "e46bea80", "b00a5631", "974c541a", "359e9963", "5c971061", "ccc07c79", "2098d9d6", "91dbd320"]
