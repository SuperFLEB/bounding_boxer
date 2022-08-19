from typing import Iterable
import bpy
from mathutils import Vector
from . import util


def _get_extremes_vectors(vectors: Iterable[Vector]) -> tuple[Vector, Vector]:
    print("GEV", vectors)
    min = [float("inf"), float("inf"), float("inf")]
    max = [-float("inf"), -float("inf"), -float("inf")]
    for vec in vectors:
        for axis in range(3):
            min[axis] = vec[axis] if vec[axis] < min[axis] else min[axis]
            max[axis] = vec[axis] if vec[axis] > max[axis] else max[axis]
    return Vector(min), Vector(max)


def get_extremes(obj: bpy.types.Object, ttl: int = 20) -> tuple[Vector, Vector]:
    """
    Find the extremes of the object, deeply incorporating instanced collections
    Note that this creates an imperfect bounding box in cases where rotation would change the world-axis
    bounding box (e.g., a rounded cube), as the untranslated bounding box is translated to world coords.
    """
    if ttl == 0:
        raise Exception("Parenting hierarchy is too deep")

    # TODO: Other sorts of parenting/instancing, too?
    if obj.instance_collection is None:
        # Regular object
        return _get_extremes_vectors([obj.matrix_local @ Vector(pt) for pt in obj.bound_box])

    extremes = []
    # Collection Instance
    for coll_obj in obj.instance_collection.objects:
        coll_extremes = get_extremes(coll_obj, ttl - 1)
        coll_extremes = [obj.matrix_local @ Vector(pt) for pt in coll_extremes]
        extremes.append(coll_extremes)
    return _get_extremes_vectors(util.flatten(extremes))


def bounds_box(extremes: tuple[Vector, Vector], name="boundbox") -> bpy.types.Object:
    """
    Create a bounding rectangular prism from two Vector points indicating extremes.
    Note that this may create an imperfect bounding box if objects are rotated. See the note on get_extremes.
    """
    vertices = [[extremes[(n >> bit) & 1][bit] for bit in range(3)] for n in range(8)]
    faces = (
        (0, 4, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 5, 1),
        (1, 5, 4, 0),
        (4, 6, 7, 5),
        (0, 2, 3, 1),
    )
    mesh = bpy.data.meshes.new(name)  # add the new mesh
    mesh.from_pydata(vertices, [], faces)
    obj = bpy.data.objects.new(name, mesh)
    return obj
