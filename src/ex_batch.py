import wmb_types

class cls_obj(object):
	
	PRIM_TRIANGLE = 4
	PRIM_TRIANGLE_STRIP = 5
	
	def __init__(self):
		"""BEG FIELDS"""
		self.id = None
		self.num_bone = None
		self.num_index = None
		self.offset_index = None
		self.offset_vertex = None
		self.offset_vertex_block = None
		self.primType = None
		self.texID = None
		self.unknownB = None
		self.unknownC = None
		self.unknownDB = None
		self.unknownE = None
		self.unknownI = None
		self.vertEnd = None
		self.vertStart = None
		"""END FIELDS"""
	
	def parse_batch(self, f):
		base_offset = self.offset_vertex_block + self.offset_vertex
		print "batch vertices offset = 0x%x" % base_offset
		if self.num_bone > 0:
			cls_vertex_format = wmb_types.cls_vertex_format_vtw
		else:
			cls_vertex_format = wmb_types.cls_vertex_format_vtw
		