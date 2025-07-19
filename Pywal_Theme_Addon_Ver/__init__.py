bl_info = {
    "name": "Pywal Theme",
    "author": "Ctoagn1",
    "version": (1, 0),
    "blender": (4, 4, 3),
    "location": "File > Apply Pywal Theme",
    "description": "Applies Pywal colors as Blender theme",
    "warning": "Requires Pywal (installed seperately), an application with full support on unix-like systems.",
    "category": "Interface",
}
        

import bpy
import os
import json
import re
import colorsys
import shutil
from bpy.types import Panel, Operator

def init_properties():
    bpy.types.Scene.axis_shift = bpy.props.BoolProperty(
        name='Apply to Axis/Grid',
        default=True
    )
    
    bpy.types.Scene.saturation_shift = bpy.props.FloatProperty(
        name='Saturation Shift',
        default=1.0,
        soft_min=0.0,
        soft_max=3.0
    )

def clear_properties():
    del bpy.types.Scene.axis_shift
    del bpy.types.Scene.saturation_shift

class MainPanel(bpy.types.Panel):
    bl_label = "Pywal Theme"
    bl_idname = "PYWAL_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pywal'
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "axis_shift")
        layout.prop(context.scene, "saturation_shift")
        layout.operator("wal.operator")
        

class WAL_operator(bpy.types.Operator):
    bl_idname = "wal.operator"
    bl_label = "Make Pywal Theme"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Makes Blender theme from Pywal colors accessible under Preferences > Themes"
    
    def modulate(self, val, mod, sat): 
        r=int(val[1:3], 16)/255.0
        g=int(val[3:5], 16)/255.0
        b=int(val[5:7], 16)/255.0
        h,l,s=colorsys.rgb_to_hls(r, g, b)
        l=max(0.0, min(1.0, l*mod))         
        s=max(0.0, min(1.0, s*sat*0.8/(mod))) 
        r, g, b=colorsys.hls_to_rgb(h, l, s)
        r=f"{int(r * 255):02x}"
        g=f"{int(g * 255):02x}"
        b=f"{int(b* 255):02x}"
        return "#"+r+g+b

    def apply_colors(self, home, workingdir, blenderversion, axis_change, saturation):
        try:
            with open (f"{home}/.cache/wal/colors.json", "r") as colorfile:
                data = json.load(colorfile)
        except FileNotFoundError:
            self.report({'ERROR'}, "Couldn't load pywal colors :(")
            return {'CANCELLED'}
        colors=data["colors"]
        tempdict=data["special"]
        colors["background"]=tempdict["background"]
        colors["foreground"]=tempdict["foreground"]

        for i in range(9,16):
            colors["color"+str(i)] = self.modulate(colors["color"+str(i)], .6, saturation)
            colors["color"+(str(i+7))] = self.modulate(colors["color"+str(i)], 1.25, saturation)
            colors["color"+(str(i+14))] = self.modulate(colors["color"+str(i)], .4, saturation)
        with open(f"{workingdir}/blendertemplate.xml", "r") as templatefile:
            contents = templatefile.read()
        for i in range(0, 26):
            contents = re.sub("color"+str(i)+"_", colors["color"+str(i)], contents)
        contents = re.sub("backgroundcolor_", colors["background"], contents)
        contents = re.sub("foregroundcolor_", colors["foreground"], contents)
        if axis_change:
            contents = re.sub("x-axis-color_", colors["color20"], contents)
            contents = re.sub("y-axis-color_", colors["color21"], contents)
            contents = re.sub("z-axis-color_", colors["color18"], contents)
            contents = re.sub("grid-color_", colors["color19"], contents)
        else:
            contents = re.sub("x-axis-color_", "#ff3352", contents)
            contents = re.sub("y-axis-color_", "#8bdc00", contents)
            contents = re.sub("z-axis-color_", "#2890ff", contents)
            contents = re.sub("grid-color_", "#545454", contents)
        os.makedirs(f"{home}/.config/blender/{blenderversion}/scripts/presets/interface_theme", exist_ok=True)
        with open(f"{home}/.config/blender/{blenderversion}/scripts/presets/interface_theme/Pywal_Theme.xml", "w") as templatefile:
            templatefile.write(contents)
        

    def execute(self, context):
        if shutil.which("wal") is None:
            self.report({'ERROR'}, "Pywal not found. This addon requires Pywal installed.")
            return {'CANCELLED'}
        workingdir = os.path.dirname(os.path.abspath(__file__))
        home = os.path.expanduser("~")
        blenderversion = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
        self.apply_colors(home, workingdir, blenderversion, context.scene.axis_shift, context.scene.saturation_shift)
        return {'FINISHED'}
    
classes = [
    MainPanel,
    WAL_operator,
]
    
def register():
    for c in classes:
        bpy.utils.register_class(c)
    init_properties()

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    clear_properties()
      
if __name__ == "__main__":
    register()

