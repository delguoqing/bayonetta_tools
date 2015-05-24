import wmb_types

class cls_obj(object):
	def __init__(self):
		"""BEG FIELDS"""
		self.id = None
		self.mat = None
		self.name = None
		self.num_batch = None
		self.offset_batch_offset_block = None
		self.unknownB = None
		self.unknownE = None
		self.unknownF = None
		self.unknownG = None
		self.unknownH = None
		self.unknwonD = None
		"""END FIELDS"""
		self.batch_offset_block = None
		self.batches = []
		
	def parse_batches(self, f):
		offset = f.tell() + self.offset_batch_offset_block
		f.seek(offset, 0)
		self.batch_offset_block = wmb_types.cls_batch_offset_block(f, self.num_batch)
		for i in xrange(self.num_batch):
			batch_offset = offset + self.batch_offset_block.offset_list[i]
			f.seek(batch_offset)
			batch = wmb_types.cls_batch(f)
			self.batches.append(batch)
	