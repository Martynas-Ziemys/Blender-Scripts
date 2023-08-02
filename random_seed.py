bl_info = {
    "name": "Random Render Seed",
    "author": "Martynas Ziemys",
    "version": (1),
    "blender": (2, 77, 0),
    "location": "CyclesRenderSettings",
    "description": "Random Render seed EVERY TIME before rendering",
    "warning": "",
    "wiki_url": ""
                "",
    "category": "Render",
}
import bpy, random
from bpy.app.handlers import persistent

@persistent
def RandomSeedHandler(scene):
    bpy.context.scene.cycles.seed = random.randint(10, 1000000000)

def register():
    bpy.app.handlers.render_pre.append(RandomSeedHandler)

def unregister():
    bpy.app.handlers.render_pre.remove(RandomSeedHandler)

if __name__ == "__main__":
    register()
