import argparse
from mot_parser import parse

if __name__ == '__main__':
	description = "Parse a mot file from Bayonetta."	
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("--mot", action="store", dest="mot_file", type=argparse.FileType("rb"), help="Input file, the Bayonetta mot file.")
	args = parser.parse_args()
	
	parse.parse(args.mot_file)