import bpy
import bmesh
import random


#################################################

number = 40          #########   THE NUMBER   #########

#################################################


previous = 0
for object in bpy.context.selected_objects:
    mesh = object.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    uv_layer = bm.loops.layers.uv.active
    offset = 1/number * random.randint(0,number - 1) 
    while offset == previous:
        offset = 1/number * random.randint(0,number - 1)
    previous = offset     
    flipx = random.randint(0, 1)
    flipy = random.randint(0, 1)  
    for face in bm.faces:
        for vert in face.loops:
            if flipx == 1:
                vert[uv_layer].uv.x = vert[uv_layer].uv.x - 0.5
                vert[uv_layer].uv.x = vert[uv_layer].uv.x * -1           
                vert[uv_layer].uv.x = vert[uv_layer].uv.x + 0.5
            if flipy == 1:
                vert[uv_layer].uv.y = vert[uv_layer].uv.y - 0.5
                vert[uv_layer].uv.y = vert[uv_layer].uv.y * -1           
                vert[uv_layer].uv.y = vert[uv_layer].uv.y + 0.5
            vert[uv_layer].uv.x = vert[uv_layer].uv.x * (1 / number) + offset            
    bm.to_mesh(mesh)