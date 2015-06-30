import six
from .mot_types import (
	cls_mot, cls_entry,
)

def parse(f):
	mot = cls_mot(f)
	
	offset_entry_end = mot.header_size + mot.num_entry * cls_entry.get_unit_size()
	
	off_assert = offset_entry_end
	mot.entries = []
	for i in range(mot.num_entry):
		entry = cls_entry(f)
		mot.entries.append(entry)
		if i == mot.num_entry - 1:
			entry.assert_null()

		