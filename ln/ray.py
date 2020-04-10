from pyrr import Vector3


class Ray:

    def __init__(self, origin: Vector3, direction: Vector3):
        self.origin = origin
        self.direction = direction

    def position(self, t) -> Vector3:
        return self.origin.add(self.direction.mulScalar(t))

    def __str__(self):
        return "O: {}, D: {}".format(self.origin, self.direction)
