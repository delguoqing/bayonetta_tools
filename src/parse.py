# -*- coding: utf8
import argparse
from wmb_types import cls_wmb

def parse(f):
	wmb = cls_wmb(f)
	wmb.post_parse(f)
	
if __name__ == '__main__':
	description = "Parse a wmb file from Bayonetta."	
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("--wmb", action="store", dest="wmb_file", type=argparse.FileType("rb"), help="Input file, the Bayonetta wmb file.")
	args = parser.parse_args()
	
	parse(args.wmb_file)