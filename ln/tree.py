from .ray import Ray
from .axis import Axis
from .hit import Hit, NoHit
from .box import Box

from pyrr import Vector3


class Tree:
    def __init__(self, box, node):
        self.box = box
        self.root = node

    @staticmethod
    def from_shapes(shapes):
        box = Box.BoxForShapes(shapes)
        node = Node(shapes)
        node.split(0)
        return Tree(box, node)

    def intersect(self, r: Ray):
        tmin, tmax = self.box.intersect(r)
        if tmax < tmin or tmax <= 0:
            return NoHit

        return self.root.intersect(r, tmin, tmax)

    def show_tree(self, level=0):
        return ' ' * level + "Tree\n" + self.root.show_tree(level + 1)


class Node:
    def __init__(self, shapes):
        self.axis = Axis.AxisNone
        self.point = 0
        self.shapes = shapes
        self.left = None
        self.right = None

    def intersect(self, r: Ray, tmin, tmax) -> Hit:
        if self.axis == Axis.AxisNone:
            return self.intersectShapes(r)

        if self.axis == Axis.AxisX:
            tsplit = (self.point - r.origin.x) / r.direction.x
            leftFirst = (r.origin.x < self.point) or (
                r.origin.x == self.point and r.direction.x <= 0)

        elif self.axis == Axis.AxisY:
            tsplit = (self.point - r.origin.y) / r.direction.y
            leftFirst = (r.origin.y < self.point) or (
                r.origin.y == self.point and r.direction.y <= 0)

        else:  # AxisZ
            tsplit = (self.point - r.origin.z) / r.direction.z
            leftFirst = (r.origin.z < self.point) or (
                r.origin.z == self.point and r.direction.z <= 0)

        if leftFirst:
            first = self.left
            second = self.right
        else:
            first = self.right
            second = self.left

        if tsplit > tmax or tsplit <= 0:
            return first.intersect(r, tmin, tmax)

        if tsplit < tmin:
            return second.intersect(r, tmin, tmax)

        h1 = first.intersect(r, tmin, tsplit)
        if h1.t <= tsplit:
            return h1

        h2 = second.intersect(r, tsplit, min(tmax, h1.t))
        if h1.t <= h2.t:
            return h1
        else:
            return h2

    def intersectShapes(self, r: Ray) -> Hit:
        hit = NoHit

        for shape in self.shapes:
            h = shape.intersect(r)
            if h.t < hit.t:
                hit = h

        return hit

    def partitionScore(self, axis: Axis, point) -> int:
        left, right = 0, 0
        for shape in self.shapes:
            box = shape.bounding_box()
            l, r = box.partition(axis, point)
            if l:
                left += 1

            if r:
                right += 1

        return max(left, right)

    def partition(self, size: int, axis: Axis, point: Vector3):
        left = []
        right = []
        for shape in self.shapes:
            box = shape.bounding_box()
            l, r = box.partition(axis, point)
            if l:
                left.append(shape)

            if r:
                right.append(shape)

        return left, right

    def split(self, depth: int):
        if len(self.shapes) < 8:
            return

        xs = []
        ys = []
        zs = []
        for shape in self.shapes:
            box = shape.bounding_box()
            xs.append(box.min.x)
            xs.append(box.max.x)
            ys.append(box.min.y)
            ys.append(box.max.y)
            zs.append(box.min.z)
            zs.append(box.max.z)

        xs.sort(key=float)
        ys.sort(key=float)
        zs.sort(key=float)

        def median(items):
            n = len(items)

            if not n:
                return 0

            if n % 2 == 1:
                return items[n / 2]

            half = int(n / 2)
            a = items[half - 1]
            b = items[half]
            return (a + b) / 2

        mx, my, mz = median(xs), median(ys), median(zs)

        best = int(len(self.shapes) * 0.85)
        bestAxis = Axis.AxisNone
        bestPoint = 0.0

        sx = self.partitionScore(Axis.AxisX, mx)
        if sx < best:
            best = sx
            bestAxis = Axis.AxisX
            bestPoint = mx

        sy = self.partitionScore(Axis.AxisY, my)
        if sy < best:
            best = sy
            bestAxis = Axis.AxisY
            bestPoint = my

        sz = self.partitionScore(Axis.AxisZ, mz)
        if sz < best:
            best = sz
            bestAxis = Axis.AxisZ
            bestPoint = mz

        if bestAxis == Axis.AxisNone:
            return

        l, r = self.partition(best, bestAxis, bestPoint)
        self.axis = bestAxis
        self.point = bestPoint
        self.left = Node(l)
        self.right = Node(r)
        self.left.split(depth + 1)
        self.right.split(depth + 1)

        self.shapes = None  # only needed at leaf nodes

    def show_tree(self, level=0):
        s = ' ' * level + "Node:"

        if self.axis == Axis.AxisNone:
            s += "Shapes ({})\n".format(len(self.shapes))
            for shape in self.shapes:
                if getattr(shape, "show_tree", None):
                    s += shape.show_tree(level + 1)

            return s

        s += "{} {:.2f}\n".format(self.axis, self.point)
        s += self.left.show_tree(level + 1)
        s += self.right.show_tree(level + 1)
        return s
