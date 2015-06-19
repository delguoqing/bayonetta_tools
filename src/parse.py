# -*- coding: utf8
import argparse
import struct
from wmb_types import cls_mesh_offset_block, cls_batch_offset_block
from wmb_types import cls_wmb, cls_mesh, cls_batch, cls_vertex_format_vtw

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
			print "\tBATCH @0x%x, vertBeg@0x%x, vertEnd@0x%x, vertNum@%d, indicesNum@%d" % \
				(batch_offset, batch.vertStart, batch.vertEnd, batch.vertEnd - batch.vertStart,
				 batch.num_index)
			batches.append(batch)
			
			vertices = []
			batch.vertices = vertices
			stride = cls_vertex_format_vtw.get_unit_size()
			for v_idx in xrange(batch.vertStart, batch.vertEnd):
				vertex_offset = wmb.offset_vertex_block + v_idx * stride
				f.seek(vertex_offset, 0)
				vf = cls_vertex_format_vtw(f)
				vertices.append(vertices)
				print "\t\t(%.2f, %.2f, %.2f)" % (vf.x, vf.y, vf.z)
	
			indices = []
			batch.indices = indices
			indices_offset = batch_offset + batch.offset_index
			f.seek(indices_offset, 0)
			for i in xrange(batch.num_index):
				indices.append(struct.unpack(">H", f.read(2))[0] - batch.vertStart)
			if batch.primType == 4:	# Triangle
				assert batch.num_index % 3 == 0, "triangle should have a index num of multiple of 3."
				for i in xrange(batch.num_index // 3):
					print indices[i * 3], indices[i * 3 + 1], indices[i * 3 + 2],
			else:
				assert batch.primType == 5, "should be 4 or 5!"
				order = 0
				# Triangle Strip
				for i in xrange(2, batch.num_index):
					if order == 0:
						print "\t\t", indices[i - 2], indices[i - 1], indices[i]
					else:
						print "\t\t", indices[i], indices[i - 1], indices[i - 2]
					order = 1 - order
			
if __name__ == '__main__':
	description = "Parse a wmb file from Bayonetta."	
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument("--wmb", action="store", dest="wmb_file", type=argparse.FileType("rb"), help="Input file, the Bayonetta wmb file.")
	args = parser.parse_args()
	
	parse(args.wmb_file)