# This is intended to use for preparing a scene copy for rendering masks.
# A full copy of the scene should be made. The script sets it up to 
# render masks in red green and blue channels of an image with cycles. 
# All scene's materials are changed to 'Masks.Black' material, then 
# materials 'Masks.Red', 'Masks.Green' and 'Masks.Blue' should be 
# assigned to desired objects. 
###############################################################################

import bpy

sc = bpy.context.scene
sc.name = "Masks"
sc.cycles.transparent_max_bounces = 0
sc.cycles.transparent_min_bounces = 0
sc.cycles.max_bounces = 0
sc.cycles.min_bounces = 0
sc.cycles.diffuse_bounces = 0
sc.cycles.glossy_bounces = 0
sc.cycles.transmission_bounces = 0
sc.cycles.volume_bounces = 0
sc.cycles.use_transparent_shadows = False
sc.cycles.caustics_reflective = False
sc.cycles.caustics_refractive = False
sc.cycles.samples = 64
sc.view_settings.view_transform = 'Default'
sc.view_settings.look = 'None'
sc.render.layers["MainLayer"].use_sky = False
sc.render.layers["MainLayer"].use_ao = False
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.image_settings.color_depth = '16'

def creataMaskMat(mat_name, color_rgba):
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
        color_rgba = (0.1, 0.1, 0.1, 1) # So it's visible in viewport
    mat.diffuse_color = color_rgba[:3]
    output_node = nodes.new('ShaderNodeOutputMaterial')
    output_node.location = (40,100)
    links = mat.node_tree.links
    link = links.new(node.outputs[0], output_node.inputs[0])

mask_materials = (
            ( ('Masks.Black'), (0, 0, 0, 1) ),
            ( ('Masks.Red'), (1, 0, 0, 1) ),
            ( ('Masks.Green'), (0, 1, 0, 1) ),
            ( ('Masks.Blue'), (0, 0, 1, 1) )
        )
        
for name, color_rgba in mask_materials:
    creataMaskMat(name, color_rgba)


for objects in bpy.context.scene.objects:
    for slots in objects.material_slots: 
        if slots.material != None:
            name = slots.material.name
            slots.link = 'OBJECT'
            slots.material = bpy.data.materials.get('Masks.Black')