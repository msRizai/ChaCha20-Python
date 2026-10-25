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
#	print(b)
	b = Rot32(b, 7)
#	print(b)

	return a, b, c, d

