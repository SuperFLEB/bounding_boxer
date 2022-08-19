import bpy
from typing import Set
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator
from ..lib import pkginfo
from ..lib import boxer
from ..lib import util

if "_LOADED" in locals():
    import importlib

    for mod in (pkginfo, boxer, util,):  # list all imports here
        importlib.reload(mod)
_LOADED = True

package_name = pkginfo.package_name()


class BoundingBoxer(Operator):
    """Make bounding box around all objects including collection instances"""
    bl_idname = "bounding_boxer.bounding_boxer"
    bl_label = "Bounding Boxer"
    bl_options = {'REGISTER', 'UNDO'}

    mesh_precision: BoolProperty(name="High-Precision Bounds on Rotated Meshes",
                                  description="Consider all points, not just bounding-box corners, so rotated meshes "
                                              "with non-square corners are calculated correctly. Increases processing.",
                                 default=True)

    @classmethod
    def poll(cls, context) -> bool:
        if len(bpy.context.selected_objects) != 1:
            cls.poll_message_set("This operator works on one object only")
            return False
        return True

    def execute(self, context) -> Set[str]:
        sel_obj = bpy.context.selected_objects[0]
        extremes = boxer.get_extremes(sel_obj, mesh_precision=self.mesh_precision)
        box = boxer.bounds_box(extremes)
        dims = extremes[1] - extremes[0]
        box.display_type = "WIRE"
        target = util.get_collection_of_object(sel_obj)
        target.objects.link(box)
        self.report({'INFO'}, f"Dimensions of bounding box: {dims}")
        return {'FINISHED'}


REGISTER_CLASSES = [BoundingBoxer]
