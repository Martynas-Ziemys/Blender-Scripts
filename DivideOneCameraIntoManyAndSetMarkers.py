bl_info = {
    "name": "Camera Split",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Search -> Camera Split",
    "description": "Camera Split",
    "warning": "",
    "wiki_url": "",
    "category": "Camera Split",
}

import bpy
from bpy.props import IntProperty


def main(context):
    for ob in context.scene.objects:
        print(ob)


class CameraSplit(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.camera_split"
    bl_label = "Camera Split"
    bl_options = {'REGISTER', 'UNDO'}
    
    n: IntProperty(
        name="Camera Grid Size",
        description="Camera split grid size",
        default = 3
    )
    @classmethod
    def poll(cls, context):
        if context.active_object is not None:
            if context.object.type == 'CAMERA':
                return True
            else:
                return False
        else:
            return False

    def execute(self, context):
        n = self.n
        bpy.ops.object.duplicate()
        data = context.object.data
        render = context.scene.render
        aspect = render.resolution_y / render.resolution_x

        data.lens = data.lens * n
        data.display_size = data.display_size / n
        data.shift_x = data.shift_x * n - (n/2 - 0.5)
        data.shift_y = (data.shift_y/aspect * n - (n/2 - 0.5))*aspect
        marker = context.scene.timeline_markers.new('',  frame=context.scene.frame_current)
        marker.camera = context.object
        context.scene.frame_current += 1
        direction = 1 
        for i in range(0, n):
            for a in range(1, n):
                bpy.ops.object.duplicate()
                marker = context.scene.timeline_markers.new('',  frame=context.scene.frame_current)
                marker.camera = context.object
                context.scene.frame_current += 1
                context.object.data.shift_x += direction
            if i<n-1:
                bpy.ops.object.duplicate()
                marker = context.scene.timeline_markers.new('',  frame=context.scene.frame_current)
                marker.camera = context.object
                context.scene.frame_current += 1
                context.object.data.shift_y += aspect
                direction = direction * - 1
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CameraSplit)


def unregister():
    bpy.utils.unregister_class(CameraSplit)


if __name__ == "__main__":
    register()

