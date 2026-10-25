from chacha20.core import Quarter_Round
def test_QuarterRound():
	a = 0x11111111
	b = 0x01020304
	c = 0x9b8d6f43
	d = 0x01234567
	assert Quarter_Round(a, b, c, d) == (0xEA2A92F4, 0xCB1CF8CE, 0x4581472E, 0x5881C4BB)

