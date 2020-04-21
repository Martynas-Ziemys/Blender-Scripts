bl_info = {
    "name": "Origin to...",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (2, 82, 0),
    "location": "3D Viewport, Alt+Shift+Ctrl+D",
    "description": "Moves the origin point to top, botom and sides of objects' bounding boxes in global space.",
    "category": "Pie Menus",
}

import bpy
from mathutils import Vector
from bpy.props import (
    BoolProperty,
    EnumProperty,
)
from bpy.types import Menu

class OBJECT_OT_origin_to(bpy.types.Operator):
    """Move the origin to top, botom or sides(global space)"""
    bl_idname = "object.origin_to"
    bl_label = "Origin to..."
    bl_options = {'REGISTER', 'UNDO'}
    
    center: BoolProperty(
        name="Center in other axis",
        description="Center in other axis",
        default=True,
    )
    move: BoolProperty(
        name="Move to 3D Cursor",
        description="Move to 3D Cursor",
        default=False,
    )
    
    sides =  (
        ('X', "X", "X"),
        ('-X', "-X", "-X"),
        ('Y', "Y", "Y"),
        ('-Y', "-Y", "-Y"),
        ('Z', "Z", "Z"),
        ('-Z', "-Z", "-Z"), 
    )
    side: EnumProperty(
        name="Side",
        items=sides,
        default='-Z',
    )

    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    def execute(self, context):
        switchMode = False
        if context.mode != 'OBJECT':
            switchMode = True
            bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
            
        for o in context.selected_objects:
            if o.type == "MESH":
                d = o.data
                m = o.matrix_world
                if self.center:
                    bounds_center = (sum((m @ Vector(b) for b in o.bound_box), Vector()))/8
                    difference = m.translation - bounds_center
                    local_difference = difference @ m
                    for v in d.vertices:
                        v.co += local_difference
                    m.translation -= difference                   

                difference = Vector((0,0,0))  
                if self.side == 'X':
                    bound = max((m @ v.co).x for v in d.vertices)
                    difference.x = m.translation.x - bound
                elif self.side == '-X':
                    bound = min((m @ v.co).x for v in d.vertices)
                    difference.x = m.translation.x - bound
                elif self.side == 'Y':
                    bound = max((m @ v.co).y for v in d.vertices)
                    difference.y = m.translation.y - bound
                elif self.side == '-Y':
                    bound = min((m @ v.co).y for v in d.vertices)
                    difference.y = m.translation.y - bound
                elif self.side == 'Z':
                    bound = max((m @ v.co).z for v in d.vertices)
                    difference.z = m.translation.z - bound
                elif self.side == '-Z':
                    bound = min((m @ v.co).z for v in d.vertices)
                    difference.z = m.translation.z - bound
                    
                local_difference = difference @ m
                for v in d.vertices:
                    v.co += local_difference
                m.translation -= difference  
                
                if self.move:
                    o.location = context.scene.cursor.location  
        if switchMode:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=True)     
                 
        return {'FINISHED'}
    
class VIEW3D_MT_PIE_origin_to_pie(Menu):
    bl_idname = "view3d.origin_to_pie"
    bl_label = "Origin to..."

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        op = pie.operator("object.origin_to", text = "Origin to Left(-X)")
        op.side = '-X'
        op.move = False
        op = pie.operator("object.origin_to", text = "Origin to Right(X)")
        op.side = 'X'
        op.move = False
        op = pie.operator("object.origin_to", text = "Origin to Bottom(-Z)")
        op.side = '-Z'
        op.move = False
        op = pie.operator("object.origin_to", text = "Origin to Top(Z)")
        op.side = 'Z'
        op.move = False
        op = pie.operator("object.origin_to", text = "Origin to Back(Y)")
        op.side = 'Y'
        op.move = False
        op = pie.operator("object.origin_to", text = "Origin to Top and cursor")
        op.side = 'Z'
        op.move = True
        op = pie.operator("object.origin_to", text = "Origin to Front(-Y)")
        op.side = '-Y'
        op.move = False
        op = pie.operator("object.origin_to", text = "Origin to Bottom and cursor")
        op.side = '-Z'
        op.move = True

addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_origin_to)
    bpy.utils.register_class(VIEW3D_MT_PIE_origin_to_pie)
    
    # handle the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new("wm.call_menu_pie", type='D', value='PRESS',shift=True, ctrl=True, alt=True)
        kmi.properties.name = "view3d.origin_to_pie"
        addon_keymaps.append((km, kmi))

def unregister():
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(OBJECT_OT_origin_to)
    bpy.utils.register_class(VIEW3D_MT_PIE_origin_to_pie)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.origin_to()
    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_origin_to")
