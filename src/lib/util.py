from typing import Iterable, Set
import bpy


def flatten(list_of_lists: Iterable[Iterable[any]]) -> list[any]:
    return [item for sublist in list_of_lists for item in sublist]


def get_collection_of_object(obj: bpy.types.Object, default_to_context: bool = True) -> bpy.types.Collection | None:
    """Get the enclosing collection of an Object (caveat: if the object is not in the active scene, this may break)"""

    # If there's only one, return that...
    candidates = [c for c in obj.users_collection]

    if len(candidates) == 0:
        return bpy.context.scene.collection if default_to_context else None

    if len(candidates) == 1:
        return candidates[0]

    # If there are more than one, but one isn't in the current Scene
    # (e.g., it's a RigidBodyWorld), return the first that isn't...
    scene_collections = [bpy.context.scene.collection] + list(bpy.context.scene.collection.children_recursive)
    candidates = [c for c in candidates if c in scene_collections]
    if len(candidates) > 0:
        return candidates[0]

    # Return the first collection from anywhere
    return obj.users_collection[0]
