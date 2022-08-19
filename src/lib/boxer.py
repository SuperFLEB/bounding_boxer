from typing import Iterable
import bpy
from mathutils import Vector
from . import util


def _get_extremes_vectors(vectors: Iterable[Vector]) -> tuple[Vector, Vector]:
    min = [float("inf"), float("inf"), float("inf")]
    max = [-float("inf"), -float("inf"), -float("inf")]
    for vec in vectors:
        for axis in range(3):
            min[axis] = vec[axis] if vec[axis] < min[axis] else min[axis]
            max[axis] = vec[axis] if vec[axis] > max[axis] else max[axis]
    return Vector(min), Vector(max)


def _get_points(obj: bpy.types.Object, mesh_precision: bool = False) -> list[Vector]:
    data_type = type(obj.data)
    if mesh_precision and type(obj.data) is bpy.types.Mesh:
        return [v.co for v in obj.data.vertices]
    else:
        return [Vector(corner) for corner in obj.bound_box]


def get_extremes(obj: bpy.types.Object, mesh_precision: bool = False, ttl: int = 20) -> tuple[Vector, Vector]:
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
        points = _get_points(obj, mesh_precision=mesh_precision)
        return _get_extremes_vectors([obj.matrix_world @ Vector(pt) for pt in points])

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
    # Each vertex is a binary (min or max) on 3 axes, so the first 3 bits of range(8) will iterate all possibilities
    # 0b001: x, 0b010: y, 0b100: z
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
