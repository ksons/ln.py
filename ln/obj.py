import numpy as np
from pyrr import Vector3

from .mesh import Mesh
from .triangle import Triangle


def parse_index(value: str, length: int) -> int:
    vi = value.split("/")
    n = int(vi[0])
    if n < 0:
        n += length

    return n


def load_obj(path: str) -> Mesh:
    with open(path, "r") as file:

        vs = []
        triangles = []

        for cnt, line in enumerate(file):

            fields = line.split()

            if len(fields) == 0:
                continue

            keyword = fields[0]
            args = fields[1:]
            # print("Line {}: {} -> {}".format(cnt, keyword, args))

            if keyword == "v":
                f = np.array(args, dtype=np.float32)
                v = Vector3(f)
                vs.append(v)
            elif keyword == "f":
                fvs = [parse_index(i, len(vs)) for i in args]
                # print("Line {}: {} -> {}".format(cnt, keyword, fvs))

                for i in range(1, len(fvs) - 1):
                    i1, i2, i3 = fvs[0], fvs[i], fvs[i + 1]

                    t = Triangle(vs[i1 - 1], vs[i2 - 1], vs[i3 - 1])
                    triangles.append(t)

        return Mesh(triangles)
