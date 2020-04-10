from pyrr import Vector3

from .hit import Hit, NoHit
from .box import Box
from .ray import Ray
from .path import Paths
from .util import vector_min, vector_max

EPS = 1e-9


class Triangle:

    def __init__(self, v1=None, v2=None, v3=None):
        self.v1 = Vector3() if v1 is None else Vector3(v1)
        self.v2 = Vector3() if v2 is None else Vector3(v2)
        self.v3 = Vector3() if v3 is None else Vector3(v3)
        self.box = None
        self.update_bounding_box()

    def compile(self):
        pass

    def bounding_box(self) -> Box:
        return self.box

    def update_bounding_box(self):
        min = vector_min(vector_min(self.v1, self.v2), self.v3)
        max = vector_max(vector_max(self.v1, self.v2), self.v3)
        self.box = Box(min, max)

    def contains(v: Vector3, f: float) -> bool:
        return False

    def intersect(self, r: Ray) -> Hit:
        e1x = self.v2.x - self.v1.x
        e1y = self.v2.y - self.v1.y
        e1z = self.v2.z - self.v1.z
        e2x = self.v3.x - self.v1.x
        e2y = self.v3.y - self.v1.y
        e2z = self.v3.z - self.v1.z
        px = r.direction.y * e2z - r.direction.z * e2y
        py = r.direction.z * e2x - r.direction.x * e2z
        pz = r.direction.x * e2y - r.direction.y * e2x
        det = e1x * px + e1y * py + e1z * pz

        if det > -EPS and det < EPS:
            return NoHit

        inv = 1 / det
        tx = r.origin.x - self.v1.x
        ty = r.origin.y - self.v1.y
        tz = r.origin.z - self.v1.z
        u = (tx * px + ty * py + tz * pz) * inv

        if u < 0.0 or u > 1.0:
            return NoHit

        qx = ty * e1z - tz * e1y
        qy = tz * e1x - tx * e1z
        qz = tx * e1y - ty * e1x
        v = (r.direction.x * qx + r.direction.y * qy + r.direction.z * qz) * inv

        if v < 0.0 or (u + v) > 1.0:
            return NoHit

        d = (e2x * qx + e2y * qy + e2z * qz) * inv
        if d < EPS:
            return NoHit

        return Hit(self, d)

    def paths(self) -> Paths:
        return Paths([
            [self.v1, self.v2],
            [self.v2, self.v3],
            [self.v3, self.v1]])

    def show_tree(self, level):
        return "%s%5.2f,%5.2f,%5.2f %5.2f,%5.2f,%5.2f %5.2f,%5.2f,%5.2f\n" % (level * ' ',
                                                                              self.v1.x, self.v1.y, self.v1.z,
                                                                              self.v2.x, self.v2.y, self.v2.z,
                                                                              self.v3.x, self.v3.y, self.v3.z)

    def __str__(self):
        return "V1: {}, V2: {}, V3: {}".format(self.v1, self.v2, self.v3)
