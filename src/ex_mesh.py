import wmb_types

class cls_obj(object):
	def __init__(self):
		"""BEG FIELDS"""
		self.id = None
		self.mat = None
		self.name = None
		self.num_batch = None
		self.num_bone = None
		self.offset_batch_offset_block = None
		self.offset_vertex_block = None
		self.unknownB = None
		self.unknownE = None
		self.unknownF = None
		self.unknownG = None
		self.unknownH = None
		self.unknwonD = None
		"""END FIELDS"""
		self.batch_offset_block = None
		self.batches = []