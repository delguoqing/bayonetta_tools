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
		
	def dump_obj(self, f):
		lod = 0
		lines = []
		start = 1
		for batch in self.batches:
			if batch.lod != lod:
				continue
			for vf in batch.vertices:
				lines.append("v %f %f %f" % (vf.x, vf.y, vf.z))
				lines.append("vt %f %f" % (vf.u, vf.v))
			if batch.primType == batch.PRIM_TRIANGLE:
				for i in xrange(batch.num_index // 3):
					idxs = batch.indices[i * 3: i * 3 + 3]
					for j in xrange(3):
						idxs[j] -= batch.vertStart - start
					lines.append("f %d %d %d" % tuple(idxs))
			elif batch.primType == batch.PRIM_TRIANGLE_STRIP:
				order = 0
				for i in xrange(2, batch.num_index):
					idxs = batch.indices[i - 2: i + 1]
					if order == 1:
						idxs.reverse()
					order = 1 - order
					idxs_combined = []
					for idx in idxs:
						idxs_combined.append(idx - batch.vertStart + start)
						idxs_combined.append(idx - batch.vertStart + start)
					lines.append("f %d/%d %d/%d %d/%d" % tuple(idxs_combined))
			else:
				assert False, "unsupported primtive type! primType=%d" % batch.primType
			start += len(batch.vertices)
		f.write("\n".join(lines))
	