import struct

# makes parsing data a lot easier
def get_getter(data, endian, force_tuple=False):
	def get(offset, fmt):
		size = struct.calcsize(fmt)
		res = struct.unpack(endian + fmt, data[offset: offset + size])
		if not force_tuple and len(res) == 1:
			return res[0]
		return res
	return get

def parse(f):
	data = f.read()
	get = get_getter(data, ">")
	FOURCC = get(0x0, "4s")
	assert FOURCC == "mot\x00", "invalid mot file"
	a, b, header_size, entry_count = get(0x4, "HHII")
	assert header_size == 0x10, "header_size != 0x10"
	print "%d, %d" % (a, b)
	
	base_offset = header_size
	for i in xrange(entry_count):
		values = get(base_offset + i * 0xc, "6h")
		print values
	
if __name__ == '__main__':
	import sys
	filepath = sys.argv[1]
	f = open(filepath, "rb")
	parse(f)
	f.close()