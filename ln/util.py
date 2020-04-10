from pyrr import Vector3
import numpy as np


def vector_min(v1: Vector3, v2: Vector3):
    return np.minimum(v1, v2)


def vector_max(v1: Vector3, v2: Vector3):
    return np.maximum(v1, v2)


def vector_min_axis(v1: Vector3) -> Vector3:
    x, y, z = [abs(v) for v in v1]
    if x <= y and x <= z:
        return Vector3([1, 0, 0])
    if y <= x and y <= z:
        return Vector3([0, 1, 0])

    return Vector3([0, 0, 1])
