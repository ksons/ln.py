from .box import Box
from .ray import Ray
from .hit import Hit, NoHit
from .path import Paths, Path

from pyrr import Vector3


class Cube:

    def __init__(self, min, max):
        self.min: Vector3 = Vector3(min)
        self.max: Vector3 = Vector3(max)
        self.box: Box = Box(self.min, self.max)

    def compile(self):
        pass

    def bounding_box(self) -> Box:
        return self.box

    def contains(self, v: Vector3, f) -> bool:

        if v.x < self.min.x - f or v.x > self.max.x + f:
            return False

        if v.Y < self.min.y - f or v.Y > self.max.y + f:
            return False

        if v.Z < self.min.z - f or v.Z > self.max.z + f:
            return False

        return True

    def intersect(self, r: Ray) -> Hit:
        n = (self.min - r.origin) / r.direction
        f = (self.max - r.origin) / r.direction

        nn = Vector3([min(n.x, f.x), min(n.y, f.y), min(n.z, f.z)])
        ff = Vector3([max(n.x, f.x), max(n.y, f.y), max(n.z, f.z)])

        t0 = max(nn.x, nn.y, nn.z)
        t1 = min(ff.x, ff.y, ff.z)
        if t0 < 1e-3 and t1 > 1e-3:
            return Hit(self, t1)

        if t0 >= 1e-3 and t0 < t1:
            return Hit(self, t0)

        return NoHit

    def paths(self) -> Paths:
        x1, y1, z1 = self.min.x, self.min.y, self.min.z
        x2, y2, z2 = self.max.x, self.max.y, self.max.z

        paths = Paths([
            Path([Vector3([x1, y1, z1]), Vector3([x1, y1, z2])]),
            Path([Vector3([x1, y1, z1]), Vector3([x1, y2, z1])]),
            Path([Vector3([x1, y1, z1]), Vector3([x2, y1, z1])]),
            Path([Vector3([x1, y1, z2]), Vector3([x1, y2, z2])]),
            Path([Vector3([x1, y1, z2]), Vector3([x2, y1, z2])]),
            Path([Vector3([x1, y2, z1]), Vector3([x1, y2, z2])]),
            Path([Vector3([x1, y2, z1]), Vector3([x2, y2, z1])]),
            Path([Vector3([x1, y2, z2]), Vector3([x2, y2, z2])]),
            Path([Vector3([x2, y1, z1]), Vector3([x2, y1, z2])]),
            Path([Vector3([x2, y1, z1]), Vector3([x2, y2, z1])]),
            Path([Vector3([x2, y1, z2]), Vector3([x2, y2, z2])]),
            Path([Vector3([x2, y2, z1]), Vector3([x2, y2, z2])]),
        ]
        )
        return paths
        # paths = paths[:0]
        # for i:
        #     = 0
        # i <= 10
        # i++ {
        #     p: = float64(i) / 10
        #     var x, y float64
        #     x = x1 + (x2-x1)*p
        #     y = y1 + (y2-y1)*p
        #     paths = append(paths, Path{{x, y1, z1}, {x, y1, z2}})
        #     paths = append(paths, Path{{x, y2, z1}, {x, y2, z2}})
        #     paths = append(paths, Path{{x1, y, z1}, {x1, y, z2}})
        #     paths = append(paths, Path{{x2, y, z1}, {x2, y, z2}})
        # }
        # return paths
