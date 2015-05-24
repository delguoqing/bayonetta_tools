import wmb_types

class cls_obj(object):
	def __init__(self):
		"""BEG FIELDS"""
		self.FOURCC = None
		self.exMatInfo = None
		self.mesh_offset_block = None
		self.numMaterials = None
		self.numVerts = None
		self.num_bone = None
		self.num_mesh = None
		self.offset_mesh_block = None
		self.offset_mesh_offset_block = None
		self.offset_vertex_block = None
		self.ofsBoneDataA = None
		self.ofsBoneDataB = None
		self.ofsBoneHie = None
		self.ofsBoneHieB = None
		self.ofsMaterials = None
		self.ofsMaterialsOfs = None
		self.ofsUnknownJ = None
		self.ofsUnknownK = None
		self.ofsUnknownL = None
		self.ofsVertExData = None
		self.unknownA = None
		self.unknownB = None
		self.unknownC = None
		self.unknownD = None
		self.unknownE = None
		self.unknownF = None
		self.unknownG = None
		self.unknownK = None
		self.unknownL = None
		"""END FIELDS"""
		self.meshes = None
		
	def post_parse(self, f):
		self.parse_meshes(f)
		
	def parse_meshes(self, f):
		self.meshes = []
		for i in xrange(self.num_mesh):
			offset = self.offset_mesh_block + self.mesh_offset_block.offset_list[i]
			f.seek(offset, 0)
			print "mesh offset 0x%x" % offset 
			mesh = wmb_types.cls_mesh(f, self.offset_vertex_block, self.num_bone)
			
			f.seek(offset, 0)
			mesh.parse_batches(f)
			self.meshes.append(mesh)
	