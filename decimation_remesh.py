'''
Copyright (C) 2018 Jean Da Costa machado.
Jean3dimensional@gmail.com

Created by Jean Da Costa machado

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import bpy
import bmesh
from mathutils.bvhtree import BVHTree
from .particle_remesher import triangle_quad_subdivide, surface_snap


class decimation_remesh(bpy.types.Operator):
    bl_idname = "tesselator2.decimation_remesh"
    bl_label = "Decimation Remesh"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    simplification = bpy.props.IntProperty(
        name="Simplification Factor",
        default=30,
        min=2,
    )
    allow_triangles = bpy.props.BoolProperty(
        name="Allow Triangles",
        description="Remesh with triangles and squares"
    )
    subdivisions = bpy.props.IntProperty(
        name="SUbdivisions",
        default=1,
        min=0
    )
    triangle_mode = bpy.props.BoolProperty(
        name="Pure Triangles",
        description="Remesh with triangles instead of squares"
    )

    @classmethod
    def poll(cls, context):
        if context.active_object:
            return context.active_object.type == "MESH" and context.active_object.mode == "OBJECT"

    def execute(self, context):
        tree = BVHTree.FromObject(context.active_object, context.scene)
        md = context.active_object.modifiers.new(type="DECIMATE", name="Decimate")
        md.ratio = 1 / self.simplification
        bpy.ops.object.modifier_apply(modifier=md.name)

        bm = bmesh.new()
        bm.from_mesh(context.active_object.data)
        bmesh.ops.triangulate(bm, faces=bm.faces)

        if not self.triangle_mode:
            bmesh.ops.join_triangles(bm, faces=bm.faces, angle_face_threshold=1.1, angle_shape_threshold=1.2)
        bm.to_mesh(context.active_object.data)

        for i in range(self.subdivisions):
            if self.triangle_mode:
                bm = bmesh.new()
                bm.from_mesh(context.active_object.data)
                bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=1, use_grid_fill=True)
                bmesh.ops.smooth_vert(bm, verts=bm.verts, use_axis_x=True, use_axis_y=True, use_axis_z=True, factor=1)
                surface_snap(bm.verts, tree)
                bm.to_mesh(context.active_object.data)

            elif self.allow_triangles:
                triangle_quad_subdivide(context.active_object)
                surface_snap(context.active_object.data.vertices, tree)
            else:

                md = context.active_object.modifiers.new(type="SUBSURF", name="Subsurf")
                md.levels = 1
                bpy.ops.object.modifier_apply(modifier=md.name)
                surface_snap(context.active_object.data.vertices, tree)
        return {"FINISHED"}
