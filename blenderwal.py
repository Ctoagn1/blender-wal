#!/usr/bin/env python3

import shutil
import os
import json
import re
import subprocess
import colorsys
import sys

def modulate(val, mod): #color lightening/darkening
    r=int(val[1:3], 16)/255.0
    g=int(val[3:5], 16)/255.0
    b=int(val[5:7], 16)/255.0
    h,l,s=colorsys.rgb_to_hls(r, g, b)
    l=max(0.0, min(1.0, l*mod)) #bounds on brightness
    r, g, b=colorsys.hls_to_rgb(h, l, s)
    r=f"{int(r * 255):02x}"
    g=f"{int(g * 255):02x}"
    b=f"{int(b* 255):02x}"
    return "#"+r+g+b

def apply_colors(home, workingdir, blenderversion):
    try:
        with open (f"{home}/.cache/wal/colors.json", "r") as file:
            data = json.load(file)
    except:
        print("Couldn't load Pywal colors :(")
        sys.exit(1)
     colors=data["colors"]
    tempdict=data["special"]
    colors["background"]=tempdict["background"]
    colors["foreground"]=tempdict["foreground"]

    for i in range(9,16):
        colors["color"+str(i)] = modulate(colors["color"+str(i)], .6)
        colors["color"+(str(i+7))] = modulate(colors["color"+str(i)], 1.25)
        colors["color"+(str(i+14))] = modulate(colors["color"+str(i)], .4)
    with open(f"{workingdir}/blendertemplate.xml", "r") as file:
        contents = file.read()
        for i in range(0, 26):
            contents = re.sub("color"+str(i)+"_", colors["color"+str(i)], contents)
        contents = re.sub("backgroundcolor", colors["background"], contents)
        contents = re.sub("foregroundcolor", colors["foreground"], contents)
        os.makedirs(f"{home}/.config/blender/{blenderversion}/scripts/presets/interface_theme", exist_ok=True)
    with open(f"{home}/.config/blender/{blenderversion}/scripts/presets/interface_theme/Pywal_Theme.xml", "w") as file:
        file.write(contents)

def main():
    workingdir = os.path.dirname(__file__)
    home = os.path.expanduser("~")
    blenderversion = subprocess.run("blender --version", shell=True, capture_output=True, text=True).stdout.strip()
    blenderversion=re.search("(Blender) ([0-9]+\\.[0-9]+)", blenderversion).group(2)
    if blenderversion == None:
        print("Blender not found or unable to identify version :(")
        sys.exit(1)
    apply_colors(home, workingdir, blenderversion)
    sys.exit(0)
if __name__ == "__main__":
    main()
