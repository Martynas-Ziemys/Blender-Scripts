bl_info = {
    "name": "Time Calculator",
    "author": "Martyans Žiemys",
    "version": (1, 0),
    "blender": (3.2, 0),
    "location": "Text Editor, side panel",
    "description": "Sums floats at the start of each line in the textblock",
    "warning": "",
    "doc_url": "",
    "category": "Text",
}


import bpy

from bpy.props import *
def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False
 
class TEXT_EDITOR_PT_Time_panel ( bpy.types.Panel ) :
 
    bl_label = "Time"
    bl_space_type = "TEXT_EDITOR"
    bl_region_type = "UI"
    bl_category = "Text"
    def draw(self, context):
        sum = 0
        layout = self.layout
        textblock = bpy.context.area.spaces.active.text
        for line in textblock.lines:
            a = line.body.split(' ')[0]
            if is_float(a):
                sum += float(a)
        layout.label(text= "    " + str(sum) + " h")
        layout.label(text= "    " + str(sum/8) + " days")
        col = layout.column()
        col.operator("text.sort_notes")
        col.operator("text.insert_79_hashes")
 
class SortNotes(bpy.types.Operator):
    """Sort Notes"""
    bl_idname = "text.sort_notes"
    bl_label = "Sort Notes"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        textblock = bpy.context.area.spaces.active.text
        tekstas = []
        tekstas2 = []
        for line in textblock.lines:
            tekstas.append(line.body)
            line.body = ''
        for l in tekstas:
            if "#" in l[:3]:
                tekstas2.append(l) 
        for l in tekstas2:
            tekstas.remove(l)
        tekstas = tekstas + tekstas2
        tekstas = filter(None, tekstas)
        textblock.clear()
        for l in tekstas:
            textblock.write("")
            textblock.write(l + "\n")
            if "#" not in l[:3]:
                textblock.write("\n")
        return {'FINISHED'}
    
class InsertPEP8LineLength(bpy.types.Operator):
    """Insert 79 hashes"""
    bl_idname = "text.insert_79_hashes"
    bl_label = "Insert PEP8 Length Line"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        textblock = bpy.context.area.spaces.active.text
        textblock.write("\n" + "#"*79 + "\n")
        return {'FINISHED'}
    
def register():
    bpy.utils.register_class(SortNotes)
    bpy.utils.register_class(InsertPEP8LineLength)
    bpy.utils.register_class(TEXT_EDITOR_PT_Time_panel)
    
def unregister():
    bpy.utils.unregister_class(SortNotes)
    bpy.utils.unregister_class(InsertPEP8LineLength)
    bpy.utils.unregister_class (TEXT_EDITOR_PT_Time_panel)

 
if __name__ == "__main__":
    register()
