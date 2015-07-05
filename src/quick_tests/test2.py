import struct
import numpy
import math

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
	print "%d, 0x%x, %d" % (a, b, get(0x4, "I"))
	entry_end = (header_size + entry_count * 0xc)
	print "entry_num = %d, entry_end = %d" % (entry_count, entry_end)
	base_offset = header_size
	last_bone_index = None
	last_frame_index = None
	now_off = entry_end
	offset_list = []
	for i in xrange(entry_count):
		values = get(base_offset + i * 0xc, "h2b2h")
		bone_index = values[0]
		frame_index = values[1]
		if i == entry_count - 1:
			break
		if bone_index != last_bone_index:
			print
		else:
			assert frame_index >= last_frame_index
		int_impl = get(base_offset + i * 0xc + 0x8, "I")
		float_impl = get(base_offset + i * 0xc + 0x8, "f")
		if values[2] == 0:
			v = float_impl
			print_track_header(values[:5] + (v, ))
		else:
			v = int_impl
			offset_list.append(v)
			print_track_header(values[:5] + (v, ))
			#assert now_off == v, "expect off=%d, off=%d" % (now_off, v)
			f = 1
			now_off += f * (12 + 4 * values[3])
			
			if values[2] == 4:
				print_frame_info_0x4(data, offset_list[-1], values[3])
			elif values[2] == 6:
				print_frame_info_0x6(data, offset_list[-1], values[3])
			elif values[2] == 1:
				print_frame_info_0x1(data, offset_list[-1], values[3])
				
		last_bone_index = bone_index
		last_frame_index = frame_index
	
	#for off1, off2 in zip(offset_list[:-1], offset_list[1:]):
	#	print "offset = 0x%x (%d), size = 0x%x" % (off1, off1, off2 - off1)
	#	print numpy.frombuffer(buffer(data[off1: off2]), dtype=numpy.dtype(">f2"))
		
def get_track_type_name(t):
	if t == 0:
		return "PosX  "
	elif t == 1:
		return "PosY  "
	elif t == 2:
		return "PosZ  "
	elif t == 3:
		return "RotX  "
	elif t == 4:
		return "RotY  "
	elif t == 5:
		return "RotZ  "
	elif t == 7:
		return "ScaleX"
	elif t == 8:
		return "ScaleY"
	elif t == 9:
		return "ScaleZ"
	return "Unknow"
	
def print_track_header(values):
	bone_idx = values[0]
	track_type = get_track_type_name(values[1])
	lerp_type = values[2]
	key_num = values[3]
	unk = values[4]
	value = values[5]
	if type(value) == float:
		v_text = "%f" % value
	else:
		v_text = "0x%x" % value
	print "BONE: %d, Type: %s, LerpType %d, KeyNum %d, %d, %s"  % (bone_idx, track_type, lerp_type,
														   key_num, unk, v_text)
	
def print_frame_info_0x4(data, offset, n):
	from util import hex_format
	get = get_getter(data, ">")
	unk_header_size = 24
	for i in xrange(3):
		unk_f0 = get(offset + i * 0x8, "f")
		print ("%.4f\t\t" % unk_f0), hex_format(data[offset + i * 0x8 + 0x4: offset + i * 0x8 + 0x8])
	
	offset += unk_header_size
	for i in xrange(n):
		base_offset = offset + i * 0x8
		unk_index, unk1, unk2, unk3 = get(base_offset, "4H")
		base_offset += 0x2
		unk_floats = numpy.frombuffer(buffer(data[base_offset : base_offset + 0x6]),
									  dtype=numpy.dtype(">f2"))
		print ("F 0x%02x:\t\t" % unk_index), hex(unk1), hex(unk2), hex(unk3)
	print
	
def print_frame_info_0x6(data, offset, n):
	from util import hex_format
	#print "\t",
	#print hex_format(data[offset: offset + 12])
	for i in xrange(3):
		values = numpy.frombuffer(buffer(data[offset + i * 4: offset + i * 4 + 4]),
							   dtype=numpy.dtype(">f2"))
		print "\t",
		print values
		
	offset += 12
	frame_idx = 0
	for i in xrange(n):
		frame_idx += ord(data[offset + i * 4])
		print "\t",
		print "F 0x%02x:\t" % frame_idx, hex_format(data[offset + i * 4: offset + i * 4 + 4])
	print
	
def print_frame_info_0x1(data, offset, n):
	print "linear interpolation: keys:",
	keys = struct.unpack(">%df" % n, data[offset: offset + 4 * n])
	print keys
	
class check_info(object):
	def __init__(self):
		self.max_track_num = 0
		self.lerp_types = set()
		self.max_key_num = 0
		self.lerp_type6_max_header_value = None
		self.lerp_type6_min_header_value = None		
	def check_max_track_num(self, v):
		self.max_track_num = max(self.max_track_num, v)
	def check_max_key_num(self, v):
		self.max_key_num = max(self.max_key_num, v)		
	def check_lerp_type(self, v):
		self.lerp_types.add(v)
	def check_lerp_type6(self, header_values):
		maxv = max(header_values)
		minv = min(header_values)
		if self.lerp_type6_max_header_value is None:
			self.lerp_type6_max_header_value = maxv
		else:
			self.lerp_type6_max_header_value = max(self.lerp_type6_max_header_value, maxv)
		if self.lerp_type6_min_header_value is None:
			self.lerp_type6_min_header_value = minv
		else:
			self.lerp_type6_min_header_value = min(self.lerp_type6_min_header_value, minv)
		
def check_frame_size(f, log=False):
	data = f.read()
	get = get_getter(data, ">")
	a, b, header_size, entry_count = get(0x4, "HHII")
	#print a, b, 
	base_offset = header_size
	entry_end = (header_size + entry_count * 0xc)	
	now_off = entry_end
	last_bone_index = None
	last_bone_index_track_num = 0
	
	ci = check_info()
	for i in xrange(entry_count):
		values = get(base_offset + i * 0xc, "h2b2h")
		
		if i == entry_count -1:
			assert values[0] == 0x7FFF
			break

		ci.check_max_track_num(values[1] + 1)
		
		if values[2] == 0:
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
				#########################
				# check header values
				# False, can't be implemented as float16
				#########################
				#header_values = numpy.frombuffer(buffer(data[off: off + 0x18]),
				#								 dtype=numpy.dtype(">f2"))
				#print header_values
				#assert not any(numpy.isnan(header_values))
				
			elif values[2] == 6:
				now_off += 12 + 4 * values[3]
				ci.check_max_key_num(values[3])
				header_values = numpy.frombuffer(buffer(data[off: off + 0xc]),
												 dtype=numpy.dtype(">f2"))				
				ci.check_lerp_type6(header_values)
			elif values[2] == 7:
				now_off += 12 + 6 * values[3]
			elif values[2] == 1:
				now_off += 4 * values[3]
			else:
				assert False, "unknown bitflag %d" % values[2]
			ci.check_lerp_type(values[2])
	return ci
			
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