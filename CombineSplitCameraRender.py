import bpy, os
from mathutils import Vector

folder = 'C:\\'
n = 3 

bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGB'
bpy.context.scene.view_settings.view_transform = 'Standard'
bpy.context.scene.view_settings.look = 'None'
def path_iterator(some_folder):
    for fp in os.listdir(some_folder):
        if fp.endswith( tuple( bpy.path.extensions_image ) ):
            yield fp
                
allimages = [] 
for imgPath in path_iterator( folder ):
    if imgPath not in bpy.data.images: 
        fullPath = os.path.join( folder, imgPath )
        img = bpy.data.images.load(fullPath)
    img = bpy.data.images.get(imgPath)
    allimages.append(img)
bpy.context.scene.render.resolution_x = img.size[0]*n
bpy.context.scene.render.resolution_y = img.size[1]*n
      
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
links = tree.links     

chunks = [allimages[x:x+n*n] for x in range(0, len(allimages), n*n)]
for i, images in enumerate(chunks):
    for every_node in tree.nodes:
        tree.nodes.remove(every_node)   
    image_location = Vector((0,0))
    offset = Vector((0,-35))    
    comp_node = tree.nodes.new('CompositorNodeComposite')   
    comp_node.location = 600,0  
    count = 0      
    for im in images:
        image_node = tree.nodes.new(type='CompositorNodeImage')
        image_node.image = im
        image_location += offset
        image_node.location = image_location 
        image_node.hide = True
        image_node.width_hidden = 60
        translate_node = tree.nodes.new(type='CompositorNodeTranslate')
        translate_node.location = image_location + Vector((170,0))
        translate_node.hide = True
        translate_node.width_hidden = 60
        translate_node.use_relative = False
        step_x = img.size[0]
        step_y = img.size[1]
        steps_side = count%n
        steps_up = count//n 
        reverse = (steps_up%2*-2)+1
        translate_node.inputs[1].default_value = -reverse*(step_x+(step_x/2)*((n+1)%2)) + step_x*steps_side*reverse
        translate_node.inputs[2].default_value = -step_y -(step_y/2)*((n+1)%2) + step_y*steps_up
        links.new(image_node.outputs[0], translate_node.inputs[0])
        if count == 0:
            last_node = translate_node
        else:
            mix_node = tree.nodes.new(type='CompositorNodeAlphaOver')
            mix_node.hide = True
            mix_node.width_hidden = 40
            mix_node.location = image_location + Vector((360,0))
            links.new(last_node.outputs[0], mix_node.inputs[1])
            links.new(translate_node.outputs[0], mix_node.inputs[2])
            last_node = mix_node
        count+=1
    links.new(last_node.outputs[0], comp_node.inputs[0])
    bpy.context.scene.render.filepath = folder + 'Comb' + str(i)
    bpy.ops.render.render(write_still=True)
