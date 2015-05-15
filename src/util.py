import os
import struct
import collections
import struct
import math
import numpy

DXT1_HEADER_TEMPLATE = "DDS |\x00\x00\x00\x07\x10\n\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00DXT1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
DXT3_HEADER_TEMPLATE = "DDS |\x00\x00\x00\x07\x10\x00\x00\x00\x08\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00DXT3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
DXT5_HEADER_TEMPLATE = "DDS |\x00\x00\x00\x07\x10\n\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x04\x00\x00\x00DXT5\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x10@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# lzss decompress
def decompress_lz01(data, init_text_buf=None, debug=False, N=4096, F=17, THRESHOLD=2, decompressed_size=None):
	text_buf = [0] * N
	
	if init_text_buf:
		init_text_buf(text_buf)
		
	dst_buf = []
	src_buf = collections.deque(map(ord, data))
	src_len = len(src_buf)
	group_idx = 0

	r = N - F - 1	# why?
	flags = 0
	bit = 0
		
	while True:
		if decompressed_size is not None:
			if len(dst_buf) == decompressed_size and (flags & 0xFF) == 0:
				break
			elif len(dst_buf) > decompressed_size:
				raise ValueError("Decompressed size do not match!")
		
		try:
			if (flags & 0x100) == 0:
				flags = src_buf.popleft() | 0xFF00
				
				if debug:
					src_offset = src_len - len(src_buf) - 1
					dst_offset = len(dst_buf)
					size = 0
					for i in xrange(8):
						if flags & (1 << i):
							size += 1
						else:
							size += 2
					print "src@offset=%s, dst@offset=%s, flags=%s, %s, size=%s" % \
						(hex(src_offset+12), hex(dst_offset), bin(flags & 0xFF), hex(flags & 0xFF), hex(size))
				bit = 0
				
			if flags & 1:
				c = src_buf.popleft()
				dst_buf.append(c)
				text_buf[r] = c
				r = (r + 1) % N
			else:
				i = src_buf.popleft()
				j = src_buf.popleft()
				offset = i | ((j & 0xF0) << 4)
				length = (j & 0xF) + THRESHOLD + 1
				copy_init = False
				if debug:
					dst_offset = len(dst_buf)
					src_offset = src_len - len(src_buf) - 2
					if dst_offset <= N:
						if (dst_offset < F and (offset >= N - F + dst_offset or offset < N - F)) or \
							(dst_offset >= F and dst_offset <= offset + F < N - F):
							print "refing init window src@offset=%s, dst@offset=%s, window@%s, size=%s" % (hex(src_offset), hex(dst_offset), hex(offset), hex(length))
							print hex(i), hex(j), hex(offset), hex(length)
							copy_init = True
					
				copied = ""
				for k in xrange(length):
					c = text_buf[(offset + k) % N]
					dst_buf.append(c)
					text_buf[r] = c
					r = (r + 1) % N
					if debug:
						copied += chr(c)
				if debug and copy_init:
					print "copied: %s" % repr(copied)
					
			flags >>= 1
			bit += 1
			
		except IndexError, e:
			if decompressed_size is not None and not (len(dst_buf) == decompressed_size and (flags & ((1 << 8 - bit) - 1)) == 0):
				print "Decompress exit with unexpected error:"
				print e
			break
	
	return "".join(map(chr, dst_buf))
	
# makes parsing data a lot easier
def get_getter(data, endian, force_tuple=False):
	def get(offset, fmt):
		size = struct.calcsize(fmt)
		res = struct.unpack(endian + fmt, data[offset: offset + size])
		if not force_tuple and len(res) == 1:
			return res[0]
		return res
	return get

# dump texture atlas layout
def quad_intersect(a, b):
	#print "compare", a, b
	if a[0] >= b[2] or b[0] >= a[2] or a[1] >= b[3] or b[1] >= a[3]:
		return False
	#print "intersect"
	return True

def dump_atlas_layout_brute_force(polys, out_fname):
	if not polys:
		return
	
	# convert raw float values to quads
	quads = []
	for fvals in polys:
		min_x = min(fvals[0: len(fvals): 2])
		max_x = max(fvals[0: len(fvals): 2])
		min_y = min(fvals[1: len(fvals): 2])
		max_y = max(fvals[1: len(fvals): 2])
		quads.append((min_x, min_y, max_x, max_y))
	
	# remove layout image of the same naming convention
	path, ext = os.path.splitext(out_fname)
	os.system("del %s*%s" % (path, ext))
	
	# seperate quads into groups
	quads_groups = [[]]
	polys_groups = [[]]
	for i, quad in enumerate(quads):
		for other_quad in quads_groups[-1]:
			if quad_intersect(quad, other_quad):
				quads_groups.append([])
				polys_groups.append([])
				break
		quads_groups[-1].append(quad)
		polys_groups[-1].append(polys[i])
		
	# dump each quads_group into a seperate atlas layout file
	for grp_idx, polys in enumerate(polys_groups):
		path, ext = os.path.splitext(out_fname)
		_dump_atlas_layout(polys, "%s%d%s" % (path, grp_idx, ext))

def dump_atlas_layout_use_mapping(polys, mapping, out_fname, ref_textures=None):
	if not polys:
		return
	
	tex_count = max(mapping.values()) + 1
	polys_groups = []
	for i in xrange(tex_count):
		polys_groups.append([])
	
	for atlas, tex in sorted(mapping.items()):
		polys_groups[tex].append( polys[atlas] )

	# remove layout image of the same naming convention
	path, ext = os.path.splitext(out_fname)
	os.system("del %s*%s" % (path, ext))
	
	# dump each quads_group into a seperate atlas layout file
	for grp_idx, polys in enumerate(polys_groups):
		path, ext = os.path.splitext(out_fname)
		ref_tex = ref_textures and ref_textures[grp_idx] or None
		_dump_atlas_layout(polys, "%s%d%s" % (path, grp_idx, ext), ref_tex)
	
def _dump_atlas_layout(polys, out_fname, ref_tex=None):
	import cairo
	min_x = min_y = 0
	max_x = max_y = 0
	for fvals in polys:
		min_x = min(min_x, min(fvals[0: len(fvals): 2]))
		max_x = max(max_x, max(fvals[0: len(fvals): 2]))
		min_y = min(min_y, min(fvals[1: len(fvals): 2]))
		max_y = max(max_y, max(fvals[1: len(fvals): 2]))
	
	WIDTH, HEIGHT = int(max_x - min_x), int(max_y - min_y)
	
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
	ctx = cairo.Context(surface)

	# paint background
	ctx.set_source_rgba(1.0, 1.0, 1.0, 0.0) # white
	ctx.rectangle(0, 0, WIDTH, HEIGHT)
	ctx.set_line_width(1.5)
	ctx.fill()

	colors = (
		(1.0, 0.0, 0.0),
		(0.0, 1.0, 0.0),
		(0.0, 0.0, 1.0),
		(0.0, 1.0, 1.0),
		(1.0, 1.0, 0.0),
		(1.0, 0.0, 1.0),
		(1.0, 0.5, 0.5),
		(0.5, 0.5, 1.0),
		(0.5, 1.0, 0.5),
	)
	
	for i, fvals in enumerate(polys):
	
		fvals = list(fvals)
		for j in xrange(0, len(fvals), 2):
			x, y = fvals[j: j + 2]
			fvals[j] = x - min_x
			fvals[j + 1] = y - min_y
			
		x0, y0 = fvals[0:2]
		x1, y1 = fvals[2:4]
		ctx.move_to(x0, y0)
		ctx.line_to(x1, y1)
		col = colors[i % len(colors)]
		ctx.set_source_rgb(*col)
		for j in xrange(4, len(fvals), 2):
			x2, y2 = fvals[j: j + 2]
			ctx.move_to(x2, y2)
			ctx.line_to(x0, y0)
			ctx.move_to(x2, y2)
			ctx.line_to(x1, y1)
			x1, y1 = x2, y2
		ctx.stroke()

	surface.write_to_png(out_fname)
	
	# mix texture
	if ref_tex:
		import Image
		ref_img = Image.open(ref_tex)
		layout_img = Image.open(out_fname)
		ref_img.paste(layout_img, (0, 0), layout_img)
		ref_img.save(out_fname)
		
def point_in_quad(x, y, quad_pos):
	p = numpy.array((x, y, 0))
	a = numpy.array(quad_pos[-1] + (0,))
	sign = None
	for pos in quad_pos:
		b = numpy.array(pos + (0,))
		ab = b - a
		ap = p - a
		ret = numpy.cross(ab, ap)
		_sign = math.copysign(1, ret[2])
		if sign is None:
			sign = _sign
		if sign * _sign < 0:
			return False
		a = b
	return True
	
def gen_dxt1_header(width, height):
	header = DXT1_HEADER_TEMPLATE
	return header[:0xc] + struct.pack("<II", height, width) + header[0x14:]

def gen_dxt3_header(width, height):
	header = DXT3_HEADER_TEMPLATE
	return header[:0xc] + struct.pack("<II", height, width) + header[0x14:]
	
def gen_dxt5_header(width, height):
	header = DXT5_HEADER_TEMPLATE
	return header[:0xc] + struct.pack("<II", height, width) + header[0x14:]
	
def decode_dxt1(data, width, height):
	pass

def decode_dxt3(data, width, height):
	pass

def decode_dxt5(data, width, height):
	pass

def hex_to_rgba(col):
	r = ((col >> 24) & 0xFF) / 255.0
	g = ((col >> 16) & 0xFF) / 255.0
	b = ((col >>  8) & 0xFF) / 255.0
	a = ((col >>  0) & 0xFF) / 255.0
	return r, g, b, a

def rgba_to_hex(r, g, b, a):
	return (int(r * 255) << 24) + (int(g * 255) << 16) + (int(b * 255) << 8) + (int(a * 255))

def hex_format(data):
	size = len(data)
	bytes_data = struct.unpack("%dB"%size, data)
	str_list = []
	for i in xrange(size / 4):
		str_list.append("%02x %02x %02x %02x" % tuple(bytes_data[i*4:i*4+4]))
	return " | ".join(str_list)

class CEmpty(object): pass

def load_simple_config(f):
	config = open(f, "r")
	obj = CEmpty()
	for k, v in eval(config.read()).iteritems():
		setattr(obj, k, v)
	return obj