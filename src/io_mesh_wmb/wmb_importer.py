# -*- coding: utf8 -*-
import os
import sys
import bmesh
import bpy
import six

def import_wmb(filepath):
	from .wmb_parser.parse import parse
	f = open(filepath, "rb")
	wmb = parse(f, False)
	f.close()
	
	hub_name = os.path.splitext(os.path.split(filepath)[1])[0]
	hub_obj = bpy.data.objects.new(hub_name, None)
	bpy.context.scene.objects.link(hub_obj)
	
	for mesh in wmb.meshes:
		for batch_idx, batch in enumerate(mesh.batches):
			# bmesh start
			bm = bmesh.new()
			if batch.lod != 0:
				continue
			#	vertices
			for vf in batch.vertices:
				bm.verts.new((vf.x, vf.z, vf.y))
			if hasattr(bm.verts, "ensure_lookup_table"):
				bm.verts.ensure_lookup_table()
			bm.verts.index_update()
			#	faces
			if batch.primType == batch.PRIM_TRIANGLE:
				for i in range(batch.num_index // 3):
					idxs = batch.indices[i * 3: i * 3 + 3]
					face = [ bm.verts[idx - batch.vertStart] for idx in idxs ]
					bm.faces.new(face)
			elif batch.primType == batch.PRIM_TRIANGLE_STRIP:
				order = 1
				for i in range(2, batch.num_index):
					idxs = batch.indices[i - 2: i + 1]
					if order == 1:
						idxs.reverse()
					order = 1 - order
					if idxs[0] == idxs[1] or idxs[0] == idxs[2] or idxs[1] == idxs[2]:
						continue					
					face = [ bm.verts[idx - batch.vertStart] for idx in idxs ]
					bm.faces.new(face)
			else:
				return {'CANCELED'}
			if hasattr(bm.faces, "ensure_lookup_table"):
				bm.faces.ensure_lookup_table()			
			bm.faces.index_update()
			# bmesh -> mesh
			name = "%s_%d" % (mesh.name.decode('ascii'), batch_idx)
			blend_mesh = bpy.data.meshes.new(name=name)
			bm.to_mesh(blend_mesh)
			# create object
			obj = bpy.data.objects.new(name, blend_mesh)
			bpy.context.scene.objects.link(obj)
			obj.parent = hub_obj
			bpy.context.scene.objects.active = obj
			bpy.ops.object.shade_smooth()
			bpy.ops.object.editmode_toggle()
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.mesh.flip_normals()
			bpy.ops.object.mode_set()
			obj.select = False
			
	return {'FINISHED'}