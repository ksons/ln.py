from pyrr import Vector3, aabb

from .axis import Axis
from .ray import Ray


class Box:

    def __init__(self, min, max):
        self._box = aabb.create_from_bounds(min, max)

    @staticmethod
    def BoxForShapes(shapes):
        if not len(shapes):
            return Box()

        boxes = [x.bounding_box()._box for x in shapes]
        nb = aabb.create_from_aabbs(boxes)

        return Box(nb[0], nb[1])

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

    @property
    def min(self):
        return Vector3(self._box[0])

    @property
    def max(self):
        return Vector3(self._box[1])

    def anchor(self, a: Vector3) -> Vector3:
        return self.min + (self.size() * a)

    def center(self) -> Vector3:
        return aabb.centre_point(self._box)

    def size(self) -> Vector3:
        return self.max - self.min

    def contains(self, b: Vector3) -> bool:
        min = self.min
        max = self.max
        return min.x <= b.x and max.x >= b.x and min.y <= b.y and \
            max.y >= b.y and min.z <= b.z and max.z >= b.z

    def extend(self, other):
        return aabb.create_from_aabbs([self._box, other._box])

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

    def __str__(self):
        return "Box: {} {}".format(self.min, self.max)
