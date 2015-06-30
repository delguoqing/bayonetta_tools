import argparse
from wmb_parser import parse

if __name__ == '__main__':
	description = "Parse a wmb file from Bayonetta."	
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("--wmb", action="store", dest="wmb_file", type=argparse.FileType("rb"), help="Input file, the Bayonetta wmb file.")
	parser.add_argument("-d", action="store_true", dest="dump_obj", default=False, help="if need dump *.obj file.")
	args = parser.parse_args()
	
	parse.parse(args.wmb_file, args.dump_obj)