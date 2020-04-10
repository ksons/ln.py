from pyrr import Vector3, Matrix44
import numpy as np

from .tree import Tree
from .ray import Ray
from .box import Box
from .path import Paths
from .hit import Hit


class Mesh:

    def __init__(self, triangles):
        self.triangles = triangles
        self.tree = None
        self.update_bounding_box()

    def compile(self):
        if not self.tree:
            shapes = []
            for triangle in self.triangles:
                shapes.append(triangle)

            self.tree = Tree.from_shapes(shapes)

    def bounding_box(self) -> Box:
        return self.box

    def contains(self, v: Vector3, f: float) -> bool:
        return False

    def intersect(self, r: Ray) -> Hit:
        return self.tree.intersect(r)

    def paths(self) -> Paths:
        result = Paths()
        for t in self.triangles:
            result.extend(t.paths()._paths)

        return result

    def update_bounding_box(self):
        self.box = Box.BoxForTriangles(self.triangles)

    def unit_cube(self):
        self.fit_inside(Box(Vector3(), Vector3([1, 1, 1])), Vector3())
        self.move_to(Vector3(), Vector3([0.5, 0.5, 0.5]))

    def move_to(self, position: Vector3, anchor: Vector3):
        matrix = Matrix44.from_translation(position - self.box.anchor(anchor))
        self.transform(matrix)

    def fit_inside(self, box: Box, anchor: Vector3):
        scale = np.amin(box.size() / self.bounding_box().size())
        extra = box.size() - (self.bounding_box().size() * scale)
        matrix = Matrix44.from_translation(-self.bounding_box().min)
        matrix = Matrix44.from_scale([scale, scale, scale]) * matrix
        matrix = Matrix44.from_translation(box.min + (extra * anchor)) * matrix
        self.transform(matrix)

    def transform(self, matrix: Matrix44):
        for t in self.triangles:
            t.v1 = matrix * t.v1
            t.v2 = matrix * t.v2
            t.v3 = matrix * t.v3
            t.update_bounding_box()

        self.update_bounding_box()
        self.tree = None

    def show_tree(self, level=0):
        return ' ' * level + "Mesh\n" + self.tree.show_tree(level + 1)
