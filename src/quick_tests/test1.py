import sys
sys.path.append("..")
import numpy
from util import get_getter

def test_vf(path):
	f = open(path, "rb")
	data = f.read()
	f.close()
	
	get = get_getter(data, ">")
	
	vert_num = get(0xc, "I")
	stride = 0x20
	offset_beg = get(0x18, "I")
	offset_end = offset_beg + vert_num * stride
	
	for offset in xrange(offset_beg, offset_end, stride):
		# pos
		x, y, z = get(offset, "fff")
		# uv
		u, v = numpy.frombuffer(buffer(data[offset + 0xc: offset + 0x10]), dtype=numpy.dtype(">f2"))
		# bone_indices
		bone_indices = get(offset + 0x18, "BBBB")
		# bone_weights
		bone_weights = get(offset + 0x1c, "BBBB")
		
		n1, n2, n3, n4 = get(offset + 0x10, "HHHH")
		u1, v1 = numpy.frombuffer(buffer(data[offset + 0x10: offset + 0x14]), dtype=numpy.dtype(">f2"))
		u2, v2 = numpy.frombuffer(buffer(data[offset + 0x14: offset + 0x18]), dtype=numpy.dtype(">f2"))
		nx, ny = get(offset + 0x10, "ff")
		print "test 0x%04x, 0x%04x, 0x%04x, 0x%04x" % (n1, n2, n3, n4)
		#print "test2 %.2f, %.2f, %.2f, %.2f" % (u1, v1, u2, v2)
		#print "uv1", u1, v1
		#print "uv2", u2, v2
		#print "test3 %f, %f" % (nx, ny)

def test_vdata_ex(path):
	f = open(path, "rb")
	data = f.read()
	f.close()
	
	get = get_getter(data, ">")
	
	vert_num = get(0xc, "I")
	stride = 0x8
	offset_beg = get(0x1c, "I")
	offset_end = offset_beg + vert_num * stride

	for offset in xrange(offset_beg, offset_end, stride):
		c = get(offset, "I")
		u1, v1 = numpy.frombuffer(buffer(data[offset + 0x4: offset + 0x8]), dtype=numpy.dtype(">f2"))
		print "color:ARGB = 0x%08x, u1 = %.2f, v2 = %.2f" % (c, u1, v1)
	
if __name__ == '__main__':
	#test_vf(r"..\..\..\..\bayonetta\data03_files\pl\pl001a\pl0031.wmb")
	#test_vf(r"..\..\..\..\bayonetta\data01_files\bm\bm000a\bm000a.wmb")
	#test_vdata_ex(r"..\..\..\..\bayonetta\data01_files\bm\bm000a\bm000a.wmb")
	#test_vdata_ex(sys.argv[1])
	test_vf(sys.argv[1])