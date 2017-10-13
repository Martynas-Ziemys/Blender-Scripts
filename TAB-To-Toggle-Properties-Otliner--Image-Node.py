# Adds TAB keyboard shortcut to toggle between Node Editor and Image Editor
# and between Properties Editor and Outliner to save screen space.
# Replaces TAB for editing Node groups with ctrl+TAB


import bpy

def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)

wm = bpy.context.window_manager
kc = wm.keyconfigs.user

# Map Property Editor
km = kc.keymaps.new('Property Editor', space_type='PROPERTIES', region_type='WINDOW', modal=False)
kmi = km.keymap_items.new('wm.context_set_enum', 'TAB', 'PRESS')
kmi_props_setattr(kmi.properties, 'data_path', 'area.type')
kmi_props_setattr(kmi.properties, 'value', 'OUTLINER')

# Map Node Generic
km = kc.keymaps.new('Node Generic', space_type='NODE_EDITOR', region_type='WINDOW', modal=False)
kmi = km.keymap_items.new('wm.context_set_enum', 'TAB', 'PRESS')
kmi_props_setattr(kmi.properties, 'data_path', 'area.type')
kmi_props_setattr(kmi.properties, 'value', 'IMAGE_EDITOR')
kmi = km.keymap_items.new('node.group_edit', 'TAB', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'exit', False)

# Map Outliner
km = kc.keymaps.new('Outliner', space_type='OUTLINER', region_type='WINDOW', modal=False)
kmi = km.keymap_items.new('wm.context_set_enum', 'TAB', 'PRESS')
kmi_props_setattr(kmi.properties, 'data_path', 'area.type')
kmi_props_setattr(kmi.properties, 'value', 'PROPERTIES')

# Map Image Generic
km = kc.keymaps.new('Image Generic', space_type='IMAGE_EDITOR', region_type='WINDOW', modal=False)
kmi = km.keymap_items.new('wm.context_set_enum', 'TAB', 'PRESS')
kmi_props_setattr(kmi.properties, 'data_path', 'area.type')
kmi_props_setattr(kmi.properties, 'value', 'NODE_EDITOR')