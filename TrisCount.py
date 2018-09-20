bl_info = {
    "name": "Tris Count",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "Space menu > Tris Count For Visible Objects",
    "description": "Counts tris",
    "warning": "",
    "wiki_url": "",
    "category": "Mesh",
    }

import bpy

class TrisCount(bpy.types.Operator):
    """Tris Count"""
    bl_idname = "scene.tris_count"
    bl_label = "Tris Count For Visible Objects"

    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):
        tris_count = 0
        for o in bpy.context.scene.objects:
            if o.type == 'MESH' and not o.hide:
                for p in o.data.polygons:
                    if len(p.vertices) > 3:
                        tris_count = tris_count + len(p.vertices) - 2
                    else:
                        tris_count = tris_count +1 
                    pass
        self.report({'INFO'}, 'Tris: ' + str(tris_count))
        return {'FINISHED'}


def register():
    bpy.utils.register_class(TrisCount)


def unregister():
    bpy.utils.unregister_class(TrisCount)


if __name__ == "__main__":
    register()
