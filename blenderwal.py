#!/usr/bin/env python3

import os
import json
import re
import subprocess
import colorsys
import sys
import argparse

def modulate(val, mod, sat): #color lightening/darkening
    r=int(val[1:3], 16)/255.0
    g=int(val[3:5], 16)/255.0
    b=int(val[5:7], 16)/255.0
    h,l,s=colorsys.rgb_to_hls(r, g, b)
    l=max(0.0, min(1.0, l*mod)) #bounds on brightness
    s=max(0.0, min(1.0, s*sat*0.8/(mod))) #darker=more saturated
    r, g, b=colorsys.hls_to_rgb(h, l, s)
    r=f"{int(r * 255):02x}"
    g=f"{int(g * 255):02x}"
    b=f"{int(b* 255):02x}"
    return "#"+r+g+b

def apply_colors(home, workingdir, blenderversion, axis_change, saturation):
    try:
        with open (f"{home}/.cache/wal/colors.json", "r") as colorfile:
            data = json.load(colorfile)
    except:
        print("Couldn't load Pywal colors :(")
        sys.exit(1)
    colors=data["colors"]
    tempdict=data["special"]
    colors["background"]=tempdict["background"]
    colors["foreground"]=tempdict["foreground"]

    for i in range(9,16):
        colors["color"+str(i)] = modulate(colors["color"+str(i)], .6, saturation)
        colors["color"+(str(i+7))] = modulate(colors["color"+str(i)], 1.25, saturation)
        colors["color"+(str(i+14))] = modulate(colors["color"+str(i)], .4, saturation)
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
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--axis', help='Changes color of axes + grid.', action='store_true')
    parser.add_argument('-s', '--saturation', type=float, action='store', help='Takes a float as an argument, adjusts saturation- default is 1, best results are usually between 0.5-2. 0 being entirely grey, and any suitably large number being eye-gratingly neon.', default=1.0)
    args = parser.parse_args()
    workingdir = os.path.dirname(__file__)
    home = os.path.expanduser("~")
    blenderversion = subprocess.run("blender --version", shell=True, capture_output=True, text=True).stdout.strip()
    blenderversion=re.search("(Blender) ([0-9]+\\.[0-9]+)", blenderversion).group(2)
    if blenderversion == None:
        print("Blender not found or unable to identify version :(")
        sys.exit(1)
    apply_colors(home, workingdir, blenderversion, args.axis, args.saturation)
    sys.exit(0)
if __name__ == "__main__":
    main()
