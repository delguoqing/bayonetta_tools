# -*- coding: utf8 -*-
import os
import sys
import bmesh
import bpy
import six
import mathutils

def import_wmb(filepath):
	from .wmb_parser.parse import parse
	f = open(filepath, "rb")
	wmb = parse(f, False)
	f.close()

	obj_name = os.path.splitext(os.path.split(filepath)[1])[0]
	
	hub_obj = import_mesh(wmb, obj_name)
	if hub_obj is None:
		return {'CANCELED'}
	armt_obj = import_armature(wmb, obj_name)
	if armt_obj is None:
		return {'CANCELED'}
	
	for obj in hub_obj.children:
		mod = obj.modifiers.new("gen_armt", 'ARMATURE')
		mod.object = armt_obj
		mod.use_bone_envelopes = False
		mod.use_vertex_groups = True
	
	return {'FINISHED'}
	
def import_mesh(wmb, hub_name):
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
				return None
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
			obj.select = True
			bpy.ops.object.shade_smooth()
			bpy.ops.object.editmode_toggle()
			bpy.ops.mesh.select_all(action='SELECT')
			bpy.ops.mesh.flip_normals()
			bpy.ops.object.mode_set()
			obj.select = False
			# create vertex groups for skinning
			for bone_idx in batch.bone_indices:
				obj.vertex_groups.new("Bone%d" % bone_idx)
			# assign vertex weights
			for v_idx, vf in enumerate(batch.vertices):
				for i, w in zip(vf.bone_indices, vf.bone_weights):
					bone_idx = batch.bone_indices[i]
					group = obj.vertex_groups["Bone%d" % bone_idx]
					group.add([v_idx], w, 'REPLACE')
			obj.hide_select = True
	return hub_obj

def import_armature(wmb, hub_name):
	armature_name = hub_name + "_armt"
	
	bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
	obj = bpy.context.object
	obj.show_x_ray = True
	obj.name = armature_name
	obj.select = True
	bpy.context.scene.objects.active = obj
	
	armt = obj.data
	armt.name = armature_name
	
	bpy.ops.object.mode_set(mode='EDIT')
	parent_list = wmb.bone_hierarchy.parent_list
	bone_pos_list = wmb.bone_offset_pos.pos_list
	print ("bone_count", len(parent_list))
	for bone_idx in range(wmb.num_bone):
		bone = armt.edit_bones.new("Bone%d" % bone_idx)
		pos = bone_pos_list[bone_idx]
		bone.head = (pos.x, pos.z, pos.y)
		bone.tail = bone.head
		bone.use_connect = False
	is_leaf = [True] * wmb.num_bone
	for bidx, pidx in enumerate(parent_list):
		bone = armt.edit_bones[bidx]
		if pidx == -1:
			bone.parent = None
		else:
			bone.parent = armt.edit_bones[pidx]
			bone.parent.tail = bone.head
			is_leaf[pidx] = False
	for bidx in range(wmb.num_bone):
		if is_leaf[bidx]:
			parent = armt.edit_bones[parent_list[bidx]]
			d = parent.tail - parent.head
			bone = armt.edit_bones[bidx]
			bone.tail = bone.head + d * 0.6
		print (bidx, bone.tail, bone.head)
	print ("leaf bone count=", is_leaf.count(True))
	bpy.ops.object.mode_set()
	return obj
