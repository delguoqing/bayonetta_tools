import sys
import glob
import test2

if __name__ == '__main__':
	index = int(sys.argv[1])
	filepath = glob.glob("../../../../bayonetta/*/*/*/*.mot")[index]
	print "parsing %s" % filepath
	f = open(filepath, "rb")
	test2.parse(f)
	f.close()