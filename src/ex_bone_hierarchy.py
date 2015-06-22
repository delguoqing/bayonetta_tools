class cls_obj(object):
	
	def __init__(self):
		"""BEG FIELDS"""
		self.num_bone = None
		self.parent_list = None
		"""END FIELDS"""
	
	def check(self):
		for parent in self.parent_list:
			assert parent == -1 or 0 <= parent < self.num_bone, "invalid bone parent %d/%d" \
															% (parent, self.num_bone)