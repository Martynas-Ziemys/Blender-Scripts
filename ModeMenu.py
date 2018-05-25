bl_info = {
    "name": "Mode Menu",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "Action Mouse button",
    "description": "Mode Menu",
    "warning": "",
    "category": "Pie Menus",
    }

import bpy
################################### operators #################################
classes = []

class MZEdgeMode(bpy.types.Operator):
    """Switch To Edge Edit Mode """
    bl_idname = "object.mz_edge_mode"
    bl_label = "Edge"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode!='EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        return {'FINISHED'}
classes.append(MZEdgeMode)

class MZFaceMode(bpy.types.Operator):
    """Switch To Face Edit Mode """
    bl_idname = "object.mz_face_mode"
    bl_label = "Face"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode!='EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        return {'FINISHED'}
classes.append(MZFaceMode)
    

class MZVertexMode(bpy.types.Operator):
    """Switch To Vertex Edit Mode """
    bl_idname = "object.mz_vertex_mode"
    bl_label = "Vertex"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode!='EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        return {'FINISHED'}
classes.append(MZVertexMode)

class MZObjectMode(bpy.types.Operator):
    """Switch To Object Mode """
    bl_idname = "object.mz_object_mode"
    bl_label = "Vertex Paint Mode"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode!='OBJECT':
            bpy.ops.object.editmode_toggle()
            if context.object.mode!='OBJECT':
                bpy.ops.object.editmode_toggle()
        return {'FINISHED'}
classes.append(MZObjectMode)
    
class MZVertexPaintMode(bpy.types.Operator):
    """Switch To Vertex Paint Mode """
    bl_idname = "object.mz_vertex_paint_mode"
    bl_label = "Vertex Paint"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode=='EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        return {'FINISHED'}
classes.append(MZVertexPaintMode)
    
class MZWeightPaintMode(bpy.types.Operator):
    """Switch To Weight Paint Mode """
    bl_idname = "object.mz_weight_paint_mode"
    bl_label = "Weight Paint"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode=='EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        return {'FINISHED'}
classes.append(MZWeightPaintMode)
    
class MZTexturePaintMode(bpy.types.Operator):
    """Switch To Texture Paint Mode """
    bl_idname = "object.mz_texture_paint_mode"
    bl_label = "Texture Paint"
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    def execute(self, context):
        if context.object.mode=='EDIT':
            bpy.ops.object.editmode_toggle()
        bpy.ops.paint.vertex_paint_toggle()
        return {'FINISHED'}
classes.append(MZTexturePaintMode)


###################################### UI #####################################

class MZModeMenu(bpy.types.Menu):
    bl_idname = "object.mode_menu"
    bl_label = "Mode Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()    
        #1
        pie.operator('object.mz_vertex_mode', text = 'Vertex', icon = 'VERTEXSEL')
        #2
        pie.operator('sculpt.sculptmode_toggle', text = 'Sculpt Mode', icon = 'SCULPTMODE_HLT')
        #3
        pie.operator('object.mz_face_mode', text = 'Face', icon = 'FACESEL')
        #4
        pie.operator('object.mz_edge_mode', text = 'Edge', icon = 'EDGESEL')
        #5
        pie.operator('object.mz_vertex_paint_mode', text = 'Vertex Paint', icon = 'VPAINT_HLT')
        #6
        pie.operator('object.mz_object_mode', text = 'Object Mode', icon = 'OBJECT_DATAMODE')
        #7
        pie.operator('object.mz_weight_paint_mode', text = 'Weight Paint', icon = 'WPAINT_HLT')
        #8
        pie.operator('object.mz_weight_paint_mode', text = 'Texture Paint', icon = 'TPAINT_HLT')
        
classes.append(MZModeMenu)
                        
################################# Registration ################################

addon_keymaps = []
def registerKeymaps():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS', shift=False, alt=False,ctrl=False)
        kmi.properties.name = "object.mode_menu"
        addon_keymaps.append((km, kmi))


def unregisterKeymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def deactivateConflictingKeymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs['Blender User']
    for km in kc.keymaps:
        if km.name == '3D View':
            for kmi in km.keymap_items:
                if kmi.name == 'Set 3D Cursor' and kmi.type == 'ACTIONMOUSE':
                    kmi.ctrl = True
 
 
def register():
    for every_class in classes:
        bpy.utils.register_class(every_class)
    registerKeymaps()
    deactivateConflictingKeymaps()


def unregister():
    unregisterKeymaps()
    for every_class in classes:
        bpy.utils.unregister_class(every_class)
        
        
if __name__ == "__main__":
    register()
