bl_info = {
    "name": "Remove Custom Transform Orientations",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (3, 6, 1),
    "location": "Search (F3) > Remove Custom Transform Orientations",
    "description": "Removes all custom transform orientations",
    "warning": "",
    "doc_url": "",
    "category": "Scene",
}

import bpy
from bpy.types import Operator

def get_custom_orientations():
    try:
        bpy.context.scene.transform_orientation_slots[0].type = ""
    except Exception as e:
        string_list = str(e).split("(")[1].replace(")", "")   
        orientation_list =  eval(f"set(({string_list}))") 
    standard_orientations = set(('GLOBAL', 'LOCAL', 'NORMAL',
                                 'GIMBAL','VIEW', 'CURSOR', 'PARENT'))
    return orientation_list - standard_orientations

def delete_custom_orientations():
    slots = bpy.context.scene.transform_orientation_slots
    for orientation in get_custom_orientations():
        slots[0].type = orientation
        bpy.ops.transform.delete_orientation()
        
class SCENE_OT_remove_custom_orientations(Operator):
    """Remove all custom transform orientations"""
    bl_idname = "scene.remove_custom_transform_orientations"
    bl_label = "Remove Custom Transform Orientations"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        delete_custom_orientations()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SCENE_OT_remove_custom_orientations)
    
def unregister():
    bpy.utils.unregister_class(SCENE_OT_remove_custom_orientations)
    
if __name__ == "__main__":
    register()