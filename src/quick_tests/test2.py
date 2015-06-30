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
	print "%d, %d, %d" % (a, b, get(0x4, "I"))
	entry_end = (header_size + entry_count * 0xc)
	print "entry_end = %d" % entry_end
	
	base_offset = header_size
	now_off = entry_end
	last_bone_index = None
	last_frame_index = None
	for i in xrange(entry_count):
		values = get(base_offset + i * 0xc, "4h")
		bone_index = values[0]
		frame_index = values[1]
		if bone_index != last_bone_index:
			print
		else:
			assert frame_index > last_frame_index
		int_impl = get(base_offset + i * 0xc + 0x8, "I")
		float_impl = get(base_offset + i * 0xc + 0x8, "f")
		if int_impl >= len(data):
			v = float_impl
		else:
			v = int_impl
		print values[:4], v
		#if i != entry_count - 1:
		#	assert values[-1] == now_off, "expect off=%d, off=%d" % (now_off, values[-1])
		now_off += 12 + 4 * values[2]
		last_bone_index = bone_index
		last_frame_index = frame_index
		
def aux_parse_wmb(f):
	data = f.read()
	get = get_getter(data, ">")
	print "bone_count", get(48, "I")
	
if __name__ == '__main__':
	import sys
	filepath = sys.argv[1]
	f = open(filepath, "rb")
	if filepath.endswith(".wmb"):
		aux_parse_wmb(f)
	else:
		parse(f)
	f.close()