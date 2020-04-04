import abc
from .box import Box

from pyrr import Vector3


class Filter(abc.ABC):
    @abc.abstractmethod
    def filter(self, v: Vector3) -> (Vector3, bool):
        pass


class ClipFilter(Filter):

    def __init__(self, matrix, eye: Vector3, scene):
        self.matrix = matrix
        self.eye = eye
        self.scene = scene
        self.clipBox = Box([-1, -1, -1], [1, 1, 1])

    def filter(self, v: Vector3) -> (Vector3, bool):
        w = self.matrix * v

        if not self.scene.visible(self.eye, v):
            return w, False

        if not self.clipBox.contains(w):
            return w, False

        return w, True
