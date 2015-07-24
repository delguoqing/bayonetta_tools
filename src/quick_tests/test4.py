import sys
import glob
import test2

def print_track_num_enum(all_ci):
	track_num_enum = {}
	for ci in all_ci:
		track_num_enum.setdefault(ci.max_track_num, 0)
		track_num_enum[ci.max_track_num] += 1
	for k, v in track_num_enum.iteritems():
		print "max_track_num %d: %d" % (k , v)
			
def print_max_key_num_enum(all_ci):
	max_key_num_enum = {}
	for ci in all_ci:
		max_key_num_enum.setdefault(ci.max_key_num, 0)
		max_key_num_enum[ci.max_key_num] += 1
	for k, v in max_key_num_enum.iteritems():
		print "max_key_num %d: %d" % (k , v)

def print_lerp_type6_header_max_min(all_ci):
	maxv = float("-inf")
	minv = float("inf")
	for ci in all_ci:
		if ci.lerp_type6_max_header_value is not None:
			maxv = max(maxv, ci.lerp_type6_max_header_value)
		if ci.lerp_type6_min_header_value is not None:
			minv = min(minv, ci.lerp_type6_min_header_value)
	print "lerp type6 header min-max", minv, maxv
	
def print_rot_value_max_min(all_ci):
	maxv = float("-inf")
	minv = float("inf")
	for ci in all_ci:
		if ci.rot_max is not None:
			maxv = max(maxv, ci.rot_max)
		if ci.rot_min is not None:
			minv = min(minv, ci.rot_min)
	print "rot immediate value min-max", minv, maxv
	
def print_lerp_type4_filename_sort_by_size(all_ci):
	def my_cmp(ci1, ci2):
		return cmp(ci1.filesize, ci2.filesize)
	all_ci.sort(cmp=my_cmp)
	for ci in all_ci:
		if ci.has_lerp_type4:
			print ci.file_index, "parsed %s, filesize=%d" % (ci.filepath, ci.filesize)

if __name__ == '__main__':
	if len(sys.argv) > 1:
		index = int(sys.argv[1])
		filepath = glob.glob("../../../../bayonetta/*/*/*/*.mot")[index]
		print "parsing %s" % filepath
		f = open(filepath, "rb")
		ci = test2.check_frame_size(f, log=True)
		all_ci = [ci]
		f.close()
	else:
		all_ci = []
		for i, filepath in enumerate(glob.glob("../../../../bayonetta/*/*/*/*.mot")):
			#print i, "parsing %s" % filepath
			f = open(filepath, "rb")
			f.seek(0, 2)
			filesize = f.tell()
			f.seek(0)			
			ci = test2.check_frame_size(f)
			ci.filepath = filepath
			ci.file_index = i
			ci.filesize = filesize
			f.close()
			all_ci.append(ci)

			#################
			# find instresting files easier
			################
			#if ci.max_key_num > 40:
			#	break
			#if 0x1 in ci.lerp_types:
			#	print i, "parsed %s" % filepath
			#if ci.has_lerp_type4:
			#	print i, "parsed %s, filesize=%d" % (filepath, filesize)
			#if ci.has_lerp_type6:
			#	assert not (ci.has_lerp_type4 and ci.has_lerp_type6)
			#	print i, "parsed %s, filesize=%d" % (filepath, filesize)

	#################
	# print out useful info
	#################
	#print_track_num_enum(all_ci)
	#print_max_key_num_enum(all_ci)
	#print_lerp_type6_header_max_min(all_ci)
	#print_rot_value_max_min(all_ci)
	print_lerp_type4_filename_sort_by_size(all_ci)