bl_info = {
    "name": "Mask Rendering",
    "author": "Martynas Žiemys",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "Alt+Ctrl+Shift+MMB",
    "description": "Makes it easy to render masks in RGB",
    "category": "Pie Menus",
    }

import bpy
classes = []


def createMaskMat(mat_name, color_rgba):
    mat = (bpy.data.materials.get(mat_name) or 
           bpy.data.materials.new(mat_name))
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    for every_node in nodes:
        nodes.remove(every_node)
    node = nodes.new('ShaderNodeEmission')
    node.location = (-190,100)
    node.inputs[0].default_value = color_rgba
    if color_rgba == (0, 0, 0, 1):
        color_rgba = (0.1, 0.1, 0.1, 1) 
    mat.diffuse_color = color_rgba[:4]
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (40,100)
    links = mat.node_tree.links
    link = links.new(node.outputs[0], output_node.inputs[0])

class SetupMasks(bpy.types.Operator):
    """Setup Masks"""
    bl_idname = "scene.setup_masks"
    bl_label = "Setup Masks"
    bl_options = {'REGISTER', 'UNDO'}
    ignore_mirror = bpy.props.BoolProperty(
            name = 'Ignore Mirror/Refractve',
            description = 'Ignore mirror and refractive materials',
            default = True
        )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.scene.name = "Masks"
        for every_object in bpy.context.scene.objects:
            for every_slot in every_object.material_slots:
                if every_slot.link !='OBJECT':
                    material = bpy.data.materials.get(every_slot.name)
                    every_slot.link = 'OBJECT'
                    every_slot.material = material

        mask_materials = (
                    ( ('Masks.Black'), (0, 0, 0, 1) ),
                    ( ('Masks.Red'), (1, 0, 0, 1) ),
                    ( ('Masks.Green'), (0, 1, 0, 1) ),
                    ( ('Masks.Blue'), (0, 0, 1, 1) )
                )
        for name, color_rgba in mask_materials:
            if name not in bpy.data.materials:
                createMaskMat(name, color_rgba)
        #Create MirrorMat
        if 'Masks.Mirror' not in bpy.data.materials:
            mat = (bpy.data.materials.get('Masks.Mirror') or 
                   bpy.data.materials.new('Masks.Mirror'))
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            for every_node in nodes:
                nodes.remove(every_node)
            node = nodes.new('ShaderNodeBsdfGlossy')
            node.location = (-190,100)
            node.distribution = 'SHARP'
            node.inputs[0].default_value = (1, 1, 1, 1)
            mat.diffuse_color = (0.5,0.5,0.5,1)
            output_node = nodes.new('ShaderNodeOutputMaterial')
            output_node.location = (40,100)
            links = mat.node_tree.links
            link = links.new(node.outputs[0], output_node.inputs[0])
        
        if 'Masks.Refractive' not in bpy.data.materials:
            mat = (bpy.data.materials.get('Masks.Refractive') or 
                   bpy.data.materials.new('Masks.Refractive'))
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            for every_node in nodes:
                nodes.remove(every_node)
            node = nodes.new('ShaderNodeBsdfRefraction')
            node.location = (-190,100)
            node.distribution = 'SHARP'
            node.inputs[0].default_value = (1, 1, 1, 1)
            output_node = nodes.new('ShaderNodeOutputMaterial')
            output_node.location = (40,100)
            links = mat.node_tree.links
            link = links.new(node.outputs[0], output_node.inputs[0])

        for objects in bpy.context.scene.objects:
            try:
                for slots in objects.material_slots: 
                    if len(objects.material_slots)>0:
                        slots.link = 'OBJECT'
                        if not (self.ignore_mirror and slots.material.name in [('Masks.Mirror'),('Masks.Refractive')]):
                            slots.material = bpy.data.materials.get('Masks.Black')
                if len(objects.material_slots)==0:
                    objects.data.materials.append(bpy.data.materials.get('Masks.Black'))
            except:
                pass
        return {'FINISHED'}
classes.append(SetupMasks)


class AssignMask(bpy.types.Operator):
    """Assign mask to the next material slot"""
    bl_idname = "object.assign_mask"
    bl_label = "Assign Mask"
    bl_options = {'REGISTER', 'UNDO'}
    original_matrial = bpy.props.StringProperty(
                name = 'Original Material',
                description = 'Original material',
                default = '',
                options = {'HIDDEN'}
            )
    last_material = bpy.props.StringProperty(
                name = 'Last Material',
                description = 'Last material',
                default = '',
                options = {'HIDDEN'}
            )
    the_object = bpy.props.StringProperty(
                name = 'Last Object',
                description = 'Last Object',
                default = '',
                options = {'HIDDEN'}
            )
    the_slot = bpy.props.IntProperty(
                name = 'Material Slot',
                description = 'Slot number mask is assigned to',
                default = 0,
                options = {'HIDDEN'}
            )
    resset = bpy.props.BoolProperty(
                name = 'Reset Material Slot',
                description = 'Reset Material Slot',
                default = False,
                options = {'HIDDEN'}
            )
    material = bpy.props.StringProperty(
                name = 'Mask Material',
                description = 'Mask Material',
                default = 'Masks.Black',
                options = {'HIDDEN'}
            )
    @classmethod
    def poll(cls, context):
        relevant_types = ['MESH','CURVE', 'SURFACE', 'META', 'FONT']
        if bpy.context.object is not None:
            if bpy.context.object.type in relevant_types:
                return True
        else:
            return False

    def execute(self, context):
        if  bpy.context.scene.name != "Masks":
            bpy.ops.scene.setup_masks()
        if self.resset:
            self.original_material = ''
            self.last_material = ''
            self.the_object = ''
            self.the_slot = 0
            self.resset = False
        else:
            if self.the_object == bpy.context.object.name:
                if self.last_material == self.material:
                    bpy.context.object.material_slots[self.the_slot].material = bpy.data.materials.get(self.original_matrial)
                self.the_slot += 1
                if self.the_slot > (len(bpy.context.object.material_slots) -1):
                    self.the_slot = 0
                while self.material == bpy.context.object.material_slots[self.the_slot].material.name:
                    self.the_slot += 1
                    if self.the_slot > (len(bpy.context.object.material_slots) -1):
                        self.the_slot = 0
                        break                             
                self.original_matrial = bpy.context.object.material_slots[self.the_slot].material.name
                bpy.context.object.material_slots[self.the_slot].material = bpy.data.materials.get(self.material)
                self.last_material = self.material                
            else:
                self.the_slot = 0
                while self.material == bpy.context.object.material_slots[self.the_slot].material.name:
                    self.the_slot += 1
                    if self.the_slot > (len(bpy.context.object.material_slots) -1):
                        self.the_slot = 0 
                        break
                self.original_matrial = bpy.context.object.material_slots[self.the_slot].material.name
                bpy.context.object.material_slots[self.the_slot].material = bpy.data.materials.get(self.material)
                self.last_material = self.material  
            self.the_object = bpy.context.object.name

        return {'FINISHED'}
classes.append(AssignMask)

class MZMasksMenu(bpy.types.Menu):
    bl_idname = "scene.masks_menu"
    bl_label = "Masks Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()    
        #1
        pie.operator('object.assign_mask', text = 'Assign Red', icon = 'COLOR_RED').material='Masks.Red'
        pie.operator('object.assign_mask', text = 'Assign Green', icon = 'COLOR_GREEN').material='Masks.Green'
        pie.operator('object.assign_mask', text = 'Assign Blue', icon = 'COLOR_BLUE').material='Masks.Blue'
        pie.operator('object.assign_mask', text = 'Assign Black').material='Masks.Black'
        pie.operator('object.assign_mask', text = 'Assign Mirror').material='Masks.Mirror'
        pie.operator('scene.scene_for_masks', text = 'Setup/reset masks', icon = 'IMAGE_ALPHA')
        pie.operator('object.assign_mask', text = 'Resset Slot Order', icon = 'FILE_REFRESH').resset=True
        pie.operator('object.assign_mask', text = 'Assign Refractive').material='Masks.Refractive'
        
classes.append(MZMasksMenu)
                    

addon_keymaps = []
def registerKeymaps():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'BUTTON5MOUSE', 'PRESS', shift=False, alt=False,ctrl=False)
        kmi.properties.name = "scene.masks_menu"
        addon_keymaps.append((km, kmi))


def unregisterKeymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

def register():
    for every_class in classes:
        bpy.utils.register_class(every_class)
    registerKeymaps()
        
def unregister():
    unregisterKeymaps()
    for every_class in classes:
        bpy.utils.unregister_class(every_class)

if __name__ == "__main__":
    register()
