bl_info = {
    "name": "Per Camera Resolution & Camera Tools",
    "author": "Martynas Žiemys",
    "version": (1, 0),
    "blender": (4, 0, 2),
    "location": "Render menu, Camera properties, 3d Viewport Shift+C",
    "description": "Renders animation with resolution per camera",
    "warning": "",
    "doc_url": "",
    "category": "Render",
}

# To do: modal adjust resolution

import bpy
from bpy.app.handlers import persistent

cls = []
camera_pie_ops = []

class MultiresolutionRender(bpy.types.Operator):
    """Render frames with resolution set from active camera"""
    bl_idname = "render.multi"
    bl_label = "Render Multiresolution Frames"
    _timer = None
    shots = None
    stop = None
    rendering = None
    filepath = None
    saved_frame = None

    def pre(self, scene, context=None):
        self.rendering = True
        
    def post(self, scene, context=None):
        self.shots.pop(0)
        self.rendering = False

    def cancelled(self, scene, context=None):
        self.stop = True

    def execute(self, context):
        self.stop = False
        self.rendering = False
        sc = context.scene
        self.saved_frame = sc.frame_current
        self.shots = [] 
        self.filepath = sc.render.filepath
        for f in range(sc.frame_start, sc.frame_end +1):
            sc.frame_set(f)
            self.shots.append([f, [sc.camera.data.res_x, sc.camera.data.res_y]])
        sc.frame_set(self.shots[0][0])
        sc.render.filepath = self.filepath + str(self.shots[0][0]).zfill(4)
        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)
        self._timer = context.window_manager.event_timer_add(
                          0.5, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
        
    def modal(self, context, event):
        if event.type == 'TIMER': 
            if True in (not self.shots, self.stop is True): 
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)
                context.scene.render.filepath = self.filepath
                context.scene.frame_set(self.saved_frame)
                return {"FINISHED"} 
            elif self.rendering is False: 
                sc = context.scene
                sc.frame_current = self.shots[0][0]
                sc.render.resolution_x = self.shots[0][1][0]
                sc.render.resolution_y = self.shots[0][1][1]
                sufix = str(self.shots[0][0]).zfill(4)
                sc.render.filepath = self.filepath + sufix
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
        return {"PASS_THROUGH"}
    
cls.append(MultiresolutionRender)

class CameraOrientationToggle(bpy.types.Operator):
    """Toggles orientation of the camera"""
    bl_idname = "camera.orientation_toggle"
    bl_label = "Camera Orientation Toggle"

    @classmethod
    def poll(cls, context):
        return context.scene.camera is not None

    def execute(self, context):
        try:
            bpy.ops.view3d.camera_to_view()
        except:
            pass
        cam = context.scene.camera.data
        cam.res_x, cam.res_y = cam.res_y, cam.res_x
        return {'FINISHED'}
    
camera_pie_ops.append(CameraOrientationToggle)
    
class SelectCam(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.select_active_cam"
    bl_label = "Select Active Camerra"
    bl_options  = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.scene.camera is not None
    
    def execute(self, context):
        try:
            bpy.ops.view3d.camera_to_view()
        except:
            pass
        bpy.ops.object.select_all(action='DESELECT')
        context.scene.camera.select_set(True)
        context.view_layer.objects.active = context.scene.camera
        return {'FINISHED'}

camera_pie_ops.append(SelectCam)

class adjust_lens(bpy.types.Operator):
    """Change focal length interactively"""
    bl_idname = "camera.adjust_lens"
    bl_label = "Lens Focal Length Adjust"
    bl_options  = {'REGISTER', 'UNDO'}
    
    first_mouse_y: bpy.props.IntProperty()
    first_value: bpy.props.FloatProperty()
    
    @classmethod
    def poll(cls, context):
        return context.scene.camera is not None
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_y - event.mouse_y
            context.object.data.lens = round(self.first_value + delta * -0.05)
        elif event.type == 'LEFTMOUSE':
            context.area.header_text_set(text = None)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.data.lens = self.first_value
            context.area.header_text_set(text = None)
            return {'CANCELLED'}
        context.area.header_text_set(text = str(round(context.object.data.lens)) + "mm")
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        try:
            bpy.ops.view3d.camera_to_view()
        except:
            pass
        bpy.context.view_layer.objects.active = context.scene.camera
        self.first_mouse_y = event.mouse_y
        self.first_value = context.object.data.lens
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

camera_pie_ops.append(adjust_lens)

class adjust_near_clip(bpy.types.Operator):
    """Adjust Camera Near Clip"""
    bl_idname = "camera.adjust_near_clip"
    bl_label = "Adjust Camera Near Clip"
    bl_options  = {'REGISTER', 'UNDO'}
    
    first_mouse_y: bpy.props.IntProperty()
    first_value: bpy.props.FloatProperty()
    
    @classmethod
    def poll(cls, context):
        return context.scene.camera is not None
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_y - event.mouse_y
            context.object.data.clip_start = self.first_value + delta * -0.005
        elif event.type == 'LEFTMOUSE':
            context.area.header_text_set(text = None)
            return {'FINISHED'}
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.data.clip_start = self.first_value
            context.area.header_text_set(text = None)
            return {'CANCELLED'}
        context.area.header_text_set(str(round(context.object.data.clip_start,3)))
        return {'RUNNING_MODAL'}
        
    def invoke(self, context, event):
        try:
            bpy.ops.view3d.camera_to_view()
        except:
            pass
        bpy.context.view_layer.objects.active = context.scene.camera
        self.first_mouse_y = event.mouse_y
        self.first_value = context.object.data.clip_start
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
camera_pie_ops.append(adjust_near_clip)

class shift_lens(bpy.types.Operator):
    """Shift Lens"""
    bl_idname = "camera.shift_lens"
    bl_label = "Shift Lens"
    bl_options  = {'REGISTER', 'UNDO'}
    first_mouse_x: bpy.props.IntProperty()
    first_value_x: bpy.props.FloatProperty()
    first_mouse_y: bpy.props.IntProperty()
    first_value_y: bpy.props.FloatProperty()
    speed: bpy.props.FloatProperty()

    @classmethod
    def poll(cls, context):
        return context.scene.camera is not None
    
    def modal(self, context, event):
        delta_x = self.first_mouse_x - event.mouse_x
        delta_y = self.first_mouse_y - event.mouse_y 
        self.speed = -0.001
        cam = context.object.data
        if event.type == 'MOUSEMOVE':
            if event.shift:
                delta_x = round(delta_x, -1)
                delta_y = round(delta_y, -1)
            elif event.ctrl:
                if abs(delta_x) > abs(delta_y):
                    delta_y = 0
                else:
                    delta_x = 0
            cam.shift_x = self.first_value_x + delta_x * self.speed
            cam.shift_y = self.first_value_y + delta_y * self.speed
        elif event.type == 'LEFTMOUSE':
            context.area.header_text_set(text = None)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            cam.shift_x = self.first_value_x
            cam.shift_y = self.first_value_y
            context.area.header_text_set(text = None)
            return {'CANCELLED'}
        elif event.type  == 'BACK_SPACE': 
            cam.shift_x = 0
            cam.data.shift_y = 0
            context.area.header_text_set(text = None)
            return {'FINISHED'}
        context.area.header_text_set(
            "Ctrl - axis constraint, Shift - snap movement," + 
            " Backspace - reset to 0 | Lens Shift X: " 
            + str(round(cam.shift_x,3)) +
            " Y: " + str(round(cam.shift_x,3))
            )

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        try:
            bpy.ops.view3d.camera_to_view()
        except:
            pass
        bpy.context.view_layer.objects.active = context.scene.camera
        self.first_mouse_x = event.mouse_x
        self.first_mouse_y = event.mouse_y
        self.first_value_x = context.object.data.shift_x
        self.first_value_y = context.object.data.shift_y
        context.window_manager.modal_handler_add(self)
        self.speed = -0.0015
        return {'RUNNING_MODAL'}
    
camera_pie_ops.append(shift_lens)

def cam_update():
    bpy.context.scene.render.resolution_x = bpy.context.scene.camera.data.res_x
    bpy.context.scene.render.resolution_y = bpy.context.scene.camera.data.res_y
    bpy.context.scene.view_settings.exposure = bpy.context.scene.camera.data.exp

def cam_update_prop(self, context):
    context.scene.render.resolution_x = context.scene.camera.data.res_x
    context.scene.render.resolution_y = context.scene.camera.data.res_y   
    context.scene.view_settings.exposure = context.scene.camera.data.exp
    
class CameraResolutionPanel(bpy.types.Panel):
        bl_label = "Camera resolution"
        bl_idname = "CAMERA_PT_resolution"
        bl_space_type = 'PROPERTIES'
        bl_region_type = 'WINDOW'
        bl_context = "data"
        
        @classmethod
        def poll(cls, context):
            return context.object.type == 'CAMERA'
        
        def draw(self, context):
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False
            camera = context.object.data
            layout.prop(camera, "exp", text="Exposure")
            col = layout.column(align=True)
            col.prop(camera, "res_x", text="Resolution X")
            col.prop(camera, "res_y", text="Y")
            row = layout.row()
            row.operator(
                "camera.orientation_toggle", 
                icon = 'FILE_REFRESH', 
                text = "Orientation Toggle")
            row.operator("render.multi",)

cls.append(CameraResolutionPanel)

class VIEW3D_MT_PIE_Camera(bpy.types.Menu):
    bl_label = "Camera Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        for op in camera_pie_ops:
            pie.operator(op.bl_idname)
        pie.prop(context.space_data, "lock_camera")
                
def draw_item(self, context):
    layout = self.layout
    layout.operator("render.multi", icon='RENDER_ANIMATION')

def handler(scene):
    try:
        scene["cam_current"]
    except:
        scene["cam_current"] = None
    if scene["cam_current"] != scene.camera: 
        cam_update()   
        scene["cam_current"]  = scene.camera  
        try:
            if bpy.context.object.type == 'CAMERA':
                bpy.context.view_layer.objects.active = scene.camera
        except:
            pass

cls.append(VIEW3D_MT_PIE_Camera)

@persistent
def camera_handler_depthgraph(scene):                    
    handler(scene)
        
@persistent
def camera_handler_framechange(scene):                      
    handler(scene)
   
addon_keymaps = [] 
def register():
    
    for c in cls + camera_pie_ops:
        bpy.utils.register_class(c)

    kcfg = bpy.context.window_manager.keyconfigs.addon
    if kcfg:
        km = kcfg.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            "wm.call_menu_pie", 
            'C', 
            'PRESS', 
            any=False, 
            alt=False, 
            ctrl=False,
            shift=True
            )
        kmi.properties.name = "VIEW3D_MT_PIE_Camera"
        addon_keymaps.append((km, kmi.idname))
        
    bpy.types.Camera.res_x = bpy.props.IntProperty(
        name='Resolution X', 
        #default=3600, # defaults screw up opened scenes
        min=4, 
        options={'ANIMATABLE'}, 
        update = cam_update_prop)     
         
    bpy.types.Camera.res_y = bpy.props.IntProperty(
        name='Resolution Y', 
        #default=2400, 
        min=4, 
        options={'ANIMATABLE'}, 
        update = cam_update_prop)
    bpy.types.Camera.exp = bpy.props.FloatProperty(
        name='Exposure', 
        default=0,  
        options={'ANIMATABLE'}, 
        update = cam_update_prop)
        
    bpy.app.handlers.depsgraph_update_post.append(camera_handler_depthgraph)
    bpy.app.handlers.frame_change_post.append(camera_handler_framechange)
    bpy.types.TOPBAR_MT_render.prepend(draw_item)

def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(camera_handler_depthgraph)
    bpy.app.handlers.frame_change_post.remove(camera_handler_framechange)
    for c in cls + camera_pie_ops:
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()