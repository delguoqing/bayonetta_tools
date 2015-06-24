# -*- coding: utf8
from __future__ import print_function
import argparse
import struct
from . import wmb_types
from .wmb_types import (
	cls_mesh_offset_block, cls_batch_offset_block,
	cls_wmb, cls_mesh, cls_batch
)

def parse(f, dump_obj):
	wmb = cls_wmb(f)
	print ("BoneNum = %d" % wmb.num_bone)
	print ("offset_bone_hierarchy = 0x%x, ofsBoneHieB = 0x%x, ofsMaterialsOfs = 0x%x, ofsMaterials = 0x%x" \
		   % (wmb.offset_bone_hierarchy, wmb.ofsBoneHieB, wmb.ofsMaterialsOfs, wmb.ofsMaterials))
	
	# mesh offset block
	f.seek(wmb.offset_mesh_offset_block, 0)
	mesh_offset_block = cls_mesh_offset_block(f, wmb.num_mesh)
	
	# bone hierarchy
	f.seek(wmb.offset_bone_hierarchy, 0)
	bone_hierarchy = wmb_types.cls_bone_hierarchy(f, wmb.num_bone)
	bone_hierarchy.check()
	
	# bone relative offset pos
	#print "bone offset: relative pos"
	f.seek(wmb.offset_bone_rel_offset_pos, 0)
	bone_rel_offset_pos = wmb_types.cls_bone_offset_pos(f, wmb.num_bone)

	# bone offset pos
	#print "bone offset: pos"
	f.seek(wmb.offset_bone_offset_pos, 0)
	bone_offset_pos = wmb_types.cls_bone_offset_pos(f, wmb.num_bone)
		
	# mesh block
	meshes = []
	wmb.meshes = meshes
	base_offset = wmb.offset_mesh_block
	for offset in mesh_offset_block.offset_list:
		offset += base_offset
		f.seek(offset, 0)
		mesh = cls_mesh(f, wmb.offset_vertex_block, wmb.num_bone)
		print ("MESH %d @0x%x" % (mesh.id, offset), end="")
		meshes.append(mesh)
		print (", name:%s" % mesh.name)
		
		offset += mesh.offset_batch_offset_block
		f.seek(offset, 0)
		batch_offset_block = cls_batch_offset_block(f, mesh.num_batch)
		
		batches = []
		mesh.batches = batches
		batch_idx = 0
		for batch_offset in batch_offset_block.offset_list:
			batch_offset += offset
			f.seek(batch_offset, 0)
			print ("\tBATCH @0x%x" % batch_offset, end="")
			batch = cls_batch(f)
			print (",vertBeg@0x%x, vertNum@%d, indicesNum@%d, lod@%d, nBone=%d, indiceOfs=0x%x, primType=%d" % \
				(batch.vertStart, batch.vertEnd - batch.vertStart,
				 batch.num_index, batch.lod, batch.num_bone, batch_offset + batch.offset_index,
				 batch.primType))
			batches.append(batch)
			
			vertices = []
			batch.vertices = vertices
			vf_cls_name = batch.get_vf_class()
			vf_cls = getattr(wmb_types, "cls_%s" % vf_cls_name)
			stride = vf_cls.get_unit_size()
			for v_idx in xrange(batch.vertStart, batch.vertEnd):
				vertex_offset = wmb.offset_vertex_block + v_idx * stride
				f.seek(vertex_offset, 0)
				vf = vf_cls(f)
				vertices.append(vf)
				#print "\t\t(%.2f, %.2f, %.2f)" % (vf.x, vf.y, vf.z)
				#print "\t\tindices:", vf.bone_indices, "weights:", vf.bone_weights
	
			indices = []
			batch.indices = indices
			indices_offset = batch_offset + batch.offset_index
			f.seek(indices_offset, 0)
			for i in xrange(batch.num_index):
				indices.append(struct.unpack(">H", f.read(2))[0])

			batch.check_bone_indices(wmb.num_bone)
			########################
			# print triangle faces
			########################
			#batch.print_faces()

			########################
			# dump lod batch to obj file
			########################
			#if batch.lod == 0:
			#	fout = open("mesh%d_%d.obj" % (mesh.id, batch_idx), "w")
			#	batch.dump_obj(fout)
			#	fout.close()
			#	batch_idx += 1

		#######################
		# dump lod0 mesh to obj file
		########################
		if dump_obj:
			fout = open("mesh%d%s.obj" % (mesh.id, mesh.name), "w")
			mesh.dump_obj(fout)
			fout.close()