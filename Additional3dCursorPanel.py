bl_info = {
    "name": "Additional 3d Cursor Panel",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "n panel, Item tab",
    "description": "Adds 3d Cursor properties to Item tab",
    "warning": "",
    "wiki_url": "",
    "category": "UI",
}

import bpy 

from bpy.types import Panel

class VIEW3D_PT_view3d_additional_cursor(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    bl_label = "3D Cursor"

    def draw(self, context):
        layout = self.layout

        cursor = context.scene.cursor

        layout.column().prop(cursor, "location", text="Location")
        rotation_mode = cursor.rotation_mode
        if rotation_mode == 'QUATERNION':
            layout.column().prop(cursor, "rotation_quaternion", text="Rotation")
        elif rotation_mode == 'AXIS_ANGLE':
            layout.column().prop(cursor, "rotation_axis_angle", text="Rotation")
        else:
            layout.column().prop(cursor, "rotation_euler", text="Rotation")
        layout.prop(cursor, "rotation_mode", text="")

def register():  
    bpy.utils.register_class(VIEW3D_PT_view3d_additional_cursor)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_view3d_additional_cursor)

if __name__ == "__main__":
    register()
