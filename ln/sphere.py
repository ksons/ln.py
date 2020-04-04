import math


from pyrr import Vector3
from .box import Box
from .ray import Ray
from .hit import Hit, NoHit
from .path import Path, Paths


class Sphere:

    def __init__(self, center=None, radius=1.0):
        self.center = Vector3() if center is None else Vector3(center)
        self.radius = radius
        radius_vec = Vector3([radius, radius, radius])
        self.box = Box(center - radius_vec, center + radius_vec)

    def compile(self):
        pass

    def bounding_box(self) -> Box:
        return self.box

    def contains(self, v: Vector3, f) -> bool:
        return (v - self.center).length() <= self.radius + f

    def intersect(self, r: Ray) -> Hit:
        radius = self.radius
        to = r.origin - self.center
        b = to | r.direction
        c = (to | to) - radius * radius
        d = b * b - c
        print(d)
        if d > 0:
            d = math.sqrt(d)
            t1 = -b - d
            if t1 > 1e-2:
                return Hit(self, t1)

            t2 = -b + d
            if t2 > 1e-2:
                return Hit(self, t2)

        return NoHit

    def paths(self) -> Paths:

        paths = Paths()
        n = 10
        o = 10
        for lat in range(-90 + o, 91 - o, n):
            path = Path()
            for lng in range(0, 361):
                v = Sphere.latlng_to_XYZ(lat, lng, self.radius) + self.center
                path.append(v)

            paths.append(path)

        for lng in range(0, 361, n):
            path = Path()
            for lat in range(-90 + o, 91 - o):
                v = Sphere.latlng_to_XYZ(lat, lng, self.radius) + self.center
                path.append(v)

            paths.append(path)

        return paths

    @staticmethod
    def latlng_to_XYZ(lat, lng, radius) -> Vector3:
        lat, lng = math.radians(lat), math.radians(lng)
        x = radius * math.cos(lat) * math.cos(lng)
        y = radius * math.cos(lat) * math.sin(lng)
        z = radius * math.sin(lat)
        return Vector3([x, y, z])
