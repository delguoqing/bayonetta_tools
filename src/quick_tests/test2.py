import struct
import numpy

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
	print "entry_num = %d, entry_end = %d" % (entry_count, entry_end)
	print "frame data len=%d" % (len(data) - entry_end)
	base_offset = header_size
	last_bone_index = None
	last_frame_index = None
	now_off = entry_end
	offset_list = []
	for i in xrange(entry_count):
		values = get(base_offset + i * 0xc, "h2b2h")
		bone_index = values[0]
		frame_index = values[1]
		if bone_index != last_bone_index:
			print
		else:
			assert frame_index > last_frame_index
		int_impl = get(base_offset + i * 0xc + 0x8, "I")
		float_impl = get(base_offset + i * 0xc + 0x8, "f")
		if values[2] == 0:
			v = float_impl
			print values[:5], v
		else:
			v = int_impl
			offset_list.append(v)
			print values[:5], hex(v)
			#assert now_off == v, "expect off=%d, off=%d" % (now_off, v)
			f = 1
			now_off += f * (12 + 4 * values[3])
		last_bone_index = bone_index
		last_frame_index = frame_index
	
	#for off1, off2 in zip(offset_list[:-1], offset_list[1:]):
	#	print "offset = 0x%x (%d), size = 0x%x" % (off1, off1, off2 - off1)
	#	print numpy.frombuffer(buffer(data[off1: off2]), dtype=numpy.dtype(">f2"))
		
def check_frame_size(f, log=False):
	data = f.read()
	get = get_getter(data, ">")
	a, b, header_size, entry_count = get(0x4, "HHII")
	#print a, b, 
	base_offset = header_size
	entry_end = (header_size + entry_count * 0xc)	
	now_off = entry_end
	for i in xrange(entry_count):
		values = get(base_offset + i * 0xc, "h2b2h")
		if i == entry_count - 1:
			assert values[0] == 0x7FFF
		elif values[2] == 0:
			values += (get(base_offset + i * 0xc + 0x8, "f"), )
			if log:
				print values
		else:
			off = get(base_offset + i * 0xc + 0x8, "I")
			values += (off, )
			if log:
				print values
			assert off == now_off
			if values[2] == 4:
				now_off += 24 + 8 * values[3]
			elif values[2] == 6:
				now_off += 12 + 4 * values[3]
			elif values[2] == 7:
				now_off += 12 + 6 * values[3]
			elif values[2] == 1:
				now_off += 4 * values[3]
			else:
				assert False, "unknown bitflag %d" % values[2]
			
			
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