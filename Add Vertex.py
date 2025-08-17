bl_info = {
    "name": "Add Vertex",
    "author": "",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > Add Vertex",
    "description": "Add Vertex",
    "warning": "",
    "wiki_url": "",
    "category": "Add Vertex",
}


import bpy
from bpy.types import Operator
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


def add_vertex(self, context):
    verts = [
        Vector((0,0,0)),
    ]
    edges = []
    faces = []
    mesh = bpy.data.meshes.new(name="Vertex")
    mesh.from_pydata(verts, edges, faces)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_vertex(Operator, AddObjectHelper):
    """Add Vertex"""
    bl_idname = "mesh.add_vertex"
    bl_label = "Add Vertex"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        add_vertex(self, context)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        return {'FINISHED'}


def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_vertex.bl_idname,
        text="Vertex",
        icon='DECORATE')


def register():
    bpy.utils.register_class(OBJECT_OT_add_vertex)
    bpy.types.VIEW3D_MT_mesh_add.prepend(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_vertex)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
