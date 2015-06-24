# -*- coding: utf8 -*-
import os
import sys

def import_wmb(filepath):
	from .wmb_parser.parse import parse
	f = open(filepath, "rb")
	wmb = parse(f, False)
	f.close()
	
#################################
# build blend mesh from neox mesh
#################################
def build_blend_mesh(geo_data, submesh_data_list):
	import bpy
	import bmesh
	for i, submesh_data in enumerate(submesh_data_list):
		# bmesh start
		bm = bmesh.new()
		# 	vertices
		for j in range(submesh_data.v_count):
			v_idx = (submesh_data.v_start + j) * 3
			co1 = geo_data.v_list[v_idx]
			co2 = geo_data.v_list[v_idx + 2]
			co3 = geo_data.v_list[v_idx + 1]
			vert = bm.verts.new((co1, co2, co3))
		bm.verts.index_update()
		# 	faces
		for j in range(submesh_data.tri_start,
						submesh_data.tri_start + submesh_data.tri_count):
			i1, i2, i3 = geo_data.tri_list[j * 3: j * 3 + 3]
			# global vertex index -> per mesh vertex index
			i1 -= submesh_data.v_start	
			i2 -= submesh_data.v_start
			i3 -= submesh_data.v_start
			bm.faces.new((bm.verts[i1], bm.verts[i2], bm.verts[i3]))
		bm.faces.index_update()
		# convert to mesh
		mesh = bpy.data.meshes.new(name=submesh_data.name)
		bm.to_mesh(mesh)
		# add uv
		for j in range(submesh_data.uv_chnl_count):
			mesh.uv_textures.new("tex%d" % j)
			for loop in mesh.loops:
				uv_idx = submesh_data.uv_start + (submesh_data.v_count * j) + loop.vertex_index
				setattr(mesh.uv_layers[j].data[loop.index], "uv", geo_data.uv_list[uv_idx * 2: uv_idx * 2 + 2])
		# create object
		obj = bpy.data.objects.new(submesh_data.name, mesh)
		bpy.context.scene.objects.link(obj)
		bpy.context.scene.objects.active = obj
		obj.select = True
