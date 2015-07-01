import sys
import glob
import test2

if __name__ == '__main__':
	if len(sys.argv) > 1:
		index = int(sys.argv[1])
		filepath = glob.glob("../../../../bayonetta/*/*/*/*.mot")[index]
		print "parsing %s" % filepath
		f = open(filepath, "rb")
		print test2.get_frame_size(f)
		f.close()
	else:
		res = {}
		for i, filepath in enumerate(glob.glob("../../../../bayonetta/*/*/*/*.mot")):
			print i, "parsing %s" % filepath
			f = open(filepath, "rb")
			size = test2.get_frame_size(f)
			f.close()
			old_v = res.setdefault(size, 0)
			res[size] = old_v + 1
			