import wmb_types

class cls_obj(object):
	
	PRIM_TRIANGLE = 4
	PRIM_TRIANGLE_STRIP = 5
	
	def __init__(self):
		"""BEG FIELDS"""
		self.bone_indices = None
		self.id = None
		self.num_bone = None
		self.num_index = None
		self.offset_index = None
		self.offset_vertex = None
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