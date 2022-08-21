# Bounding Boxer

https://github.com/SuperFLEB/bounding_boxer

A Blender addon that creates a bounding box around an object, including any instanced collections.

This was a quick-and-dirty addon made to test, tweak, and visualize the code in `lib/boxer.py`, so I
could use it in the [Kiro](https://github.com/SuperFLEB/kiro) project to measure collection instances
for proper spacing (because Collection Instances present themselves present as single-point Empty objects).

## To install

There's probably not a release for this, but I left the `build_release.py` script in there so you can
make one. Just clone it and run `build_release.py` with whatever copy of Python 3 you've got
hanging around, and install the resulting ZIP file into Blender.

## To use

Select one object. There's a "Bounding Boxer" menuitem in the object context menu.

The "High-Precision Bounds on Rotated Meshes" option (default on) will use and transform all points in a
mesh to determine the bounds, instead of just the bounding box. This helps the case where the bounding box
would change after rotation is applied, such as with a heavily-beveled cube rotated to stand on a corner.
(The new top, bottom, and sides would not take the trimmed corners into account.)
