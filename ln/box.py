from .axis import Axis
from .ray import Ray

from pyrr import Vector3


class Box:

    def __init__(self, min=None, max=None):
        self.min: Vector3 = Vector3() if min is None else Vector3(min)
        self.max: Vector3 = Vector3() if max is None else Vector3(max)

    @staticmethod
    def BoxForShapes(shapes):
        if not len(shapes):
            return Box()

        box = shapes[0].bounding_box()
        for shape in shapes:
            box = box.extend(shape.bounding_box())

        return box

    @staticmethod
    def BoxForTriangles(shapes):
        return Box.BoxForShapes(shapes)

    @staticmethod
    def BoxForVectors(vectors):
        if not len(vectors) == 0:
            return Box()

        min = vectors[0]
        max = vectors[0]
        for vector in vectors:
            min = min.Min(vector)
            max = max.Max(vector)

        return Box(min, max)

    def anchor(self, a: Vector3) -> Vector3:
        return self.min.Add(self.size().Mul(a))

    def center(self) -> Vector3:
        return self.anchor(Vector3(0.5, 0.5, 0.5))

    def size(self) -> Vector3:
        return self.max - self.min

    def contains(self, b: Vector3) -> bool:
        return self.min.x <= b.x and self.max.x >= b.x and self.min.y <= b.y and \
            self.max.y >= b.y and self.min.z <= b.z and self.max.z >= b.z

    def extend(self, other):
        minimum = Vector3([min(self.min.x, other.min.x), min(
            self.min.y, other.min.y), min(self.min.z, other.min.z)])
        maximum = Vector3([max(self.max.x, other.max.x), max(
            self.max.y, other.max.y), min(self.max.z, other.max.z)])
        return Box(minimum, maximum)

    def intersect(self, r: Ray):
        x1 = (self.min.x - r.origin.x) / r.direction.x
        y1 = (self.min.y - r.origin.y) / r.direction.y
        z1 = (self.min.z - r.origin.z) / r.direction.z
        x2 = (self.max.x - r.origin.x) / r.direction.x
        y2 = (self.max.y - r.origin.y) / r.direction.y
        z2 = (self.max.z - r.origin.z) / r.direction.z

        if x1 > x2:
            x1, x2 = x2, x1

        if y1 > y2:
            y1, y2 = y2, y1

        if z1 > z2:
            z1, z2 = z2, z1

        t1 = max(max(x1, y1), z1)
        t2 = min(min(x2, y2), z2)
        return t1, t2

    def partition(self, axis: Axis, point) -> (bool, bool):
        if axis == Axis.AxisX:
            left = self.min.x <= point
            right = self.max.x >= point
        elif axis == Axis.AxisY:
            left = self.min.y <= point
            right = self.max.y >= point
        else:
            left = self.min.z <= point
            right = self.max.z >= point

        return left, right
