# -*- coding: utf8 -*-
import os
import sys
import glob
from util import get_getter

def unpack_file(fname):
	f = open(fname, "rb")
	data = f.read()
	f.close()
	
	get = get_getter(data, ">")
	FOURCC = get(0x0, "4s")
	assert FOURCC == "DAT\x00"
	file_count = get(0x4, "I")
	blk_file_off_off, blk_ext_off, blk_filename_off, blk_file_size_off = get(0x8, "IIII")
	dummys = get(0x18, "II")
	assert not any(dummys)

	# basicly no use
	ext_list = []
	offset = blk_ext_off
	for i in xrange(file_count):
		term_off = data.find("\x00", offset)
		ext = data[offset: term_off]
		offset = term_off + 1
		ext_list.append(ext)
	
	# create folders to put unpacked files in
	folder = os.path.splitext(fname)[0]
	if not os.path.isdir(folder):
		os.mkdir(folder)
		
	# extract files
	filename_len = get(blk_filename_off, "I")
	for i in xrange(file_count):
		name = get(blk_filename_off + 0x4 + i * filename_len, "%ds" % filename_len).rstrip("\x00")
		file_off = get(blk_file_off_off + i * 0x4, "I")
		file_size = get(blk_file_size_off + i * 0x4, "I")
		if file_size > 0:
			file_data = data[file_off: file_off + file_size]
			file_path = os.path.join(folder, name)
			fout = open(file_path, "wb")
			fout.write(file_data)
			fout.close()
			
def unpack(path):
	if os.path.isdir(path):
		for fname in glob.glob(os.path.join(path, "*.dat")):
			unpack_file(fname)
		for fname in glob.glob(os.path.join(path, "*/*.dat")):
			unpack_file(fname)
	elif os.path.isfile(path):
		unpack_file(path)
		
if __name__ == '__main__':
	unpack(sys.argv[1])