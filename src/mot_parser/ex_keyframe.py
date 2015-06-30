class cls_obj(object):
	
	def __init__(self):
		"""BEG FIELDS"""
		self.bone_index = None
		self.frame_index = None
		self.offset = None
		self.unk2 = None
		self.unk3 = None
		"""END FIELDS"""
		pass
		
	def assert_null(self):
		assert self.bone_index == 0x7FFF and self.frame_index == -1 \
			and not any((self.unk2, self.unk3, self.unk4, self.unk5)), "should be null entry."
	