bl_info = {
    "name": "Place Active Copies on Selected",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (3, 6, 4),
    "location": "View3D > Object > Link\Transfer Data(Ctrl+L)",
    "description": "Place active copies on selected",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy.props import StringProperty

class OBJECT_OT_copy_to_selected(Operator):
    """Place active object copies on selected"""
    bl_idname = "object.copies_to_selected"
    bl_label = "Place Active Copies on Selected"
    bl_options = {'REGISTER', 'UNDO'}

    offset: FloatVectorProperty(
        name="Offset",
        default=(0.0, 0.0, 0.0),
        subtype='TRANSLATION',
        description="offset",
    )
    name: StringProperty(
        name="Name",
        default="",
        description="Name of copies",
    )

    def execute(self, context):
        C=context
        active = C.object
        selected = C.selected_objects
        for o in selected:
            if o is active: #skip active itself
                continue
            obj_copy = active.copy()
            C.collection.objects.link(obj_copy)
            obj_copy.location = o.location + self.offset
            obj_copy.name = self.name
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.name = context.object.name
        return self.execute(context)

def copy_to_selected_button(self, context):
    self.layout.operator(OBJECT_OT_copy_to_selected.bl_idname, icon='PLUGIN')


def register():
    bpy.utils.register_class(OBJECT_OT_copy_to_selected)
    bpy.types.VIEW3D_MT_make_links.append(copy_to_selected_button)

def unregister():
    bpy.types.VIEW3D_MT_make_links.remove(copy_to_selected_button)
    bpy.utils.unregister_class(OBJECT_OT_copy_to_selected)

if __name__ == "__main__":
    register()
