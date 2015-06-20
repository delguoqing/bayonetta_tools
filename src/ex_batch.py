import operator
import wmb_types

class cls_obj(object):
	
	PRIM_TRIANGLE = 4
	PRIM_TRIANGLE_STRIP = 5
	
	def __init__(self):
		"""BEG FIELDS"""
		self.bone_indices = None
		self.id = None
		self.lod = None
		self.num_bone = None
		self.num_index = None
		self.offset_index = None
		self.offset_vertex = None
		self.primType = None
		self.texID = None
		self.unknownC = None
		self.unknownDB = None
		self.unknownE = None
		self.unknownI = None
		self.vertEnd = None
		self.vertStart = None
		self.vertex_format = None
		"""END FIELDS"""
		self.vertices = []
		self.indices = []

	def print_faces(self):
		if batch.primType == self.PRIM_TRIANGLE:	# Triangle
			assert batch.num_index % 3 == 0, "triangle should have a index num of multiple of 3."
			for i in xrange(batch.num_index // 3):
				print indices[i * 3], indices[i * 3 + 1], indices[i * 3 + 2],
		else:
			assert batch.primType == self.PRIM_TRIANGLE_STRIP, "should be 4 or 5!"
			order = 0
			# Triangle Strip
			for i in xrange(2, batch.num_index):
				if order == 0:
					print "\t\t", indices[i - 2], indices[i - 1], indices[i]
				else:
					print "\t\t", indices[i], indices[i - 1], indices[i - 2]
				order = 1 - order
			
	def dump_obj(self, f):
		lines = []
		for vf in self.vertices:
			lines.append("v %f %f %f" % (vf.x, vf.y, vf.z))
		for vf in self.vertices:
			lines.append("vt %f %f" % (vf.u, vf.v))
		if self.primType == self.PRIM_TRIANGLE:
			for i in xrange(self.num_index // 3):
				idxs = self.indices[i * 3: i * 3 + 3]
				for j in xrange(3):
					idxs[j] -= self.vertStart - 1
				lines.append("f %d %d %d" % tuple(idxs))
		elif self.primType == self.PRIM_TRIANGLE_STRIP:
			order = 0
			for i in xrange(2, self.num_index):
				idxs = self.indices[i - 2: i + 1]
				if order == 1:
					idxs.reverse()
				order = 1 - order
				idxs_combined = []
				for idx in idxs:
					idxs_combined.append(idx - self.vertStart + 1)
					idxs_combined.append(idx - self.vertStart + 1)
				lines.append("f %d/%d %d/%d %d/%d" % tuple(idxs_combined))
		else:
			assert False, "unsupported primtive type! primType=%d" % self.primType
		f.write("\n".join(lines))
		
	def get_vf_class(self):
		if self.vertex_format & 0x1:
			return wmb_types.cls_vertex_format_vtw
		else:
			return wmb_types.cls_vertex_format_vt