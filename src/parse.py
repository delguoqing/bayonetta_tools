# -*- coding: utf8
import argparse
from wmb_types import cls_mesh_offset_block, cls_batch_offset_block
from wmb_types import cls_wmb, cls_mesh, cls_batch

def parse(f):
	wmb = cls_wmb(f)
	
	# mesh offset block
	f.seek(wmb.offset_mesh_offset_block, 0)
	mesh_offset_block = cls_mesh_offset_block(f, wmb.num_mesh)
	
	# mesh block
	meshes = []
	wmb.meshes = meshes
	base_offset = wmb.offset_mesh_block
	for offset in mesh_offset_block.offset_list:
		offset += base_offset
		print "MESH @0x%x" % offset
		f.seek(offset, 0)
		mesh = cls_mesh(f, wmb.offset_vertex_block, wmb.num_bone)
		meshes.append(mesh)
		
		offset += mesh.offset_batch_offset_block
		f.seek(offset, 0)
		batch_offset_block = cls_batch_offset_block(f, mesh.num_batch)
		
		batches = []
		mesh.batches = batches
		for batch_offset in batch_offset_block.offset_list:
			batch_offset += offset
			f.seek(batch_offset, 0)
			batch = cls_batch(f)
			print "\tBATCH @0x%x, vertBeg@0x%x, vertEnd@0x%x" % (batch_offset, batch.vertStart,
																 batch.vertEnd)
			batches.append(batch)
			
	
if __name__ == '__main__':
	description = "Parse a wmb file from Bayonetta."	
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("--wmb", action="store", dest="wmb_file", type=argparse.FileType("rb"), help="Input file, the Bayonetta wmb file.")
	args = parser.parse_args()
	
	parse(args.wmb_file)