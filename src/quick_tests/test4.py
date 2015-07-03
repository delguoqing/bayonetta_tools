import sys
import glob
import test2

if __name__ == '__main__':
	if len(sys.argv) > 1:
		index = int(sys.argv[1])
		filepath = glob.glob("../../../../bayonetta/*/*/*/*.mot")[index]
		print "parsing %s" % filepath
		f = open(filepath, "rb")
		max_track_num = test2.check_frame_size(f, log=True)
		print "max_track_num = %d" % max_track_num
		f.close()
	else:
		track_num_enum = {}
		for i, filepath in enumerate(glob.glob("../../../../bayonetta/*/*/*/*.mot")):
			print i, "parsing %s" % filepath
			f = open(filepath, "rb")
			max_track_num = test2.check_frame_size(f)
			if max_track_num == 30:
				break
			track_num_enum.setdefault(max_track_num, 0)
			track_num_enum[max_track_num] += 1
			f.close()
			
		for k, v in track_num_enum.iteritems():
			print "max_track_num %d: %d" % (k , v)
		