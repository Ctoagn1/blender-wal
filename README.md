# blender-wal
![alt text](https://github.com/Ctoagn1/blender-wal/blob/main/images/purple.png?raw=true)
![alt text](https://github.com/Ctoagn1/blender-wal/blob/main/images/red.png?raw=true)
![alt text](https://github.com/Ctoagn1/blender-wal/blob/main/images/yellow-green.png?raw=true)

Pywal addon for Blender themes

  I'm indecisive and feel the need to change my wallpaper every five minutes, so it helps having some scripts that can automate applying a matching color palette to the stuff I use. Add to your wallpaper manager or just run it manually whenever you swap wallpapers- it should appear in blender under Preferences as Pywal Theme. Alternatively, install Pywal_Theme.zip as an addon in Blender for built-in functionality, including all customization options that the script offers.

By virtue of the theme not using set colors and instead using whatever your wallpaper is, some themes will look better than others, but I've gotten some pretty nice ones.

See `https://github.com/Ctoagn1/Blender-Wallpaper-for-all/` for a similar blender addon that works on windows/mac/linux and doesn't require pywal or any of its backends. (In order to be dependency-free, it uses the colorz backend locally with a weighted k-mean. Stick with this one if you prefer other backends. This was designed with ImageMagick in mind.)

# Usage Guide

**Install:**  `git clone https://github.com/Ctoagn1/blender-wal`
Move the script and xml to a directory of your choosing- it should work, as long as they're together. chmod +x if necessary, and you should be good to go. If you're using the addon, simply go to Preferences > Add-ons > Install from Disk.

**Dependencies:**  Blender, python, and pywal. Which, if you're interested in using this, you probably already have. 

**Features:** You can pass `-a` or `--axis` as an argument to the script in order to change the xyz-axes and grid to fit the theme. It's off by default, as I didn't want to make it too intrusive (though personally, I prefer it on). You can also pass `-s` or `--saturation` along with a float to change how saturated the colors are- default is 1, and you'll find the best results between 0.5-2, but feel free to put whatever number you like.


Credit to https://github.com/hayyaoe/zenities for the dots in the photos
