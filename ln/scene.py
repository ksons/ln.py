from .hit import Hit
from .tree import Tree
from .ray import Ray
from .path import Paths
from .filter import ClipFilter

from pyrr import Matrix44, Vector3, vector


class Scene:
    def __init__(self):
        self.shapes = []
        self.tree = None

    def compile(self):
        for shape in self.shapes:
            shape.compile()

        if not self.tree:
            self.tree = Tree.from_shapes(self.shapes)

    def add(self, shape):
        self.shapes.append(shape)

    def intersect(self, r) -> Hit:
        return self.tree.intersect(r)

    def visible(self, eye: Vector3, point: Vector3) -> bool:
        v = eye - point
        vn = vector.normalize(v)
        r = Ray(point, Vector3(vn))
        hit = self.intersect(r)
        return hit.t >= vector.length(v)

    def paths(self) -> Paths:
        result = Paths()
        for shape in self.shapes:
            result.extend(shape.paths()._paths)

        return result

    def Render(self, eye: Vector3, center: Vector3, up: Vector3, width, height, fovy, near, far, step) -> Paths:
        aspect = width / height
        matrix = Matrix44.look_at(eye, center, up)
        matrix = Matrix44.perspective_projection(
            fovy, aspect, near, far) * matrix
        return self.RenderWithMatrix(matrix, eye, width, height, step)

    def RenderWithMatrix(self, matrix: Matrix44, eye: Vector3, width, height, step) -> Paths:
        self.compile()
        paths = self.paths()

        if step > 0:
            paths = paths.chop(step)

        paths = paths.filter(ClipFilter(matrix, eye, self))
        if step > 0:
            paths = paths.simplify(1e-6)

        translation = Matrix44.from_translation([1, 1, 0])
        scale = Matrix44.from_scale([width / 2, height / 2, 0])
        matrix = scale * translation

        paths = paths.transform(matrix)
        return paths
