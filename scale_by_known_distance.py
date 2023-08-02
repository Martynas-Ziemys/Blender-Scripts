bl_info = {
    "name": "Scale By Known Distance",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "View3D search -> Scale By Known Distance, "\
                "View3D -> Object -> Transform / Mesh -> Mransform",
    "description": "Scales mesh by known distance between 2 vertices",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
from bpy.props import FloatProperty
from math import dist


class OBJECT_OT_known_distance(bpy.types.Operator):
    """Scales selected objects by known distance between 2 verts"""
    bl_idname = "object.scale_by_known_distance"
    bl_label = "Scale By Known Distance "
    bl_options = {'REGISTER', 'UNDO'}
    l : FloatProperty(name = "Distance between vertices: ", default = 0)
    distance = 0
    
    @classmethod
    def poll(cls, context):
        return context.active_object.type == 'MESH'

    def execute(self, context):
        o = bpy.context.object
        scale = self.l / self.distance 
        bpy.ops.object.mode_set(mode = 'OBJECT')
        context.scene.tool_settings.transform_pivot_point = 'ACTIVE_ELEMENT'
        bpy.ops.transform.resize(value = (scale,scale,scale))
        self.report({"INFO"}, str(scale))
        self.report({"INFO"}, f"Scaled {self.distance:.4f} to " \
                              f"{self.distance*scale:.4f} ({scale:.4f})")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        o = bpy.context.object
        o.update_from_editmode()
        sel = [v for v in o.data.vertices if v.select]
        if len(sel) != 2:
            self.report({"WARNING"}, "Select 2 vertices!")
            return {'CANCELLED'}
        v1,v2 = sel
        self.l = dist(o.matrix_world @ v1.co, o.matrix_world @ v2.co)
        self.distance = self.l
        return context.window_manager.invoke_props_dialog(self, width = 450)

        
def known_distance_button(self, context):
    self.layout.operator(OBJECT_OT_known_distance.bl_idname, icon='PLUGIN')
        

def register():
    bpy.utils.register_class(OBJECT_OT_known_distance)
    bpy.types.VIEW3D_MT_transform_object.append(known_distance_button)
    bpy.types.VIEW3D_MT_transform.append(known_distance_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_known_distance)
    bpy.types.VIEW3D_MT_transform_object.remove(known_distance_button)
    bpy.types.VIEW3D_MT_transform.remove(known_distance_button)

if __name__ == "__main__":
    register()