import sys
import glob
import test2

if __name__ == '__main__':
	if len(sys.argv) > 1:
		index = int(sys.argv[1])
		filepath = glob.glob("../../../../bayonetta/*/*/*/*.mot")[index]
		print "parsing %s" % filepath
		f = open(filepath, "rb")
		test2.check_frame_size(f, log=True)
		f.close()
	else:
		for i, filepath in enumerate(glob.glob("../../../../bayonetta/*/*/*/*.mot")):
			print i, "parsing %s" % filepath
			f = open(filepath, "rb")
			test2.check_frame_size(f)
			f.close()			