import bpy

n = 3
bpy.ops.object.duplicate()
data = bpy.context.object.data
render = bpy.context.scene.render
aspect = render.resolution_y / render.resolution_x

data.lens = data.lens * n
data.display_size = data.display_size / n
data.shift_x = data.shift_x * n - (n/2 - 0.5)
data.shift_y = (data.shift_y/aspect * n - (n/2 - 0.5))*aspect
marker = bpy.context.scene.timeline_markers.new('',  frame=bpy.context.scene.frame_current)
marker.camera = bpy.context.object
bpy.context.scene.frame_current += 1
direction = 1 
for i in range(0, n):
    for a in range(1, n):
        bpy.ops.object.duplicate()
        marker = bpy.context.scene.timeline_markers.new('',  frame=bpy.context.scene.frame_current)
        marker.camera = bpy.context.object
        bpy.context.scene.frame_current += 1
        bpy.context.object.data.shift_x += direction
    if i<n-1:
        bpy.ops.object.duplicate()
        marker = bpy.context.scene.timeline_markers.new('',  frame=bpy.context.scene.frame_current)
        marker.camera = bpy.context.object
        bpy.context.scene.frame_current += 1
        bpy.context.object.data.shift_y += aspect
        direction = direction * - 1
