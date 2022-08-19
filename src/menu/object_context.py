import bpy
from ..operator import bounding_boxer

if "_LOADED" in locals():
    import importlib

    for mod in (an_operator,):  # list all imports here
        importlib.reload(mod)
_LOADED = True


class BoundingBoxerSubmenu(bpy.types.Menu):
    bl_idname = 'bounding_boxer.bounding_boxer'
    bl_label = 'Bounding Boxer'

    def draw(self, context) -> None:
        self.layout.operator(an_operator.BoundingBoxer.bl_idname)


REGISTER_CLASSES = [BoundingBoxerSubmenu]
