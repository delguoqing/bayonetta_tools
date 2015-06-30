class cls_obj(object):
	
	def __init__(self):
		"""BEG FIELDS"""
		self.unk0 = None
		self.unk1 = None
		self.unk2 = None
		self.unk3 = None
		self.unk4 = None
		self.unk5 = None
		"""END FIELDS"""
		pass
		
	def assert_null(self):
		assert self.unk0 == 0x7FFF and self.unk1 == -1 \
			and not any((self.unk2, self.unk3, self.unk4, self.unk5)), "should be null entry."
	