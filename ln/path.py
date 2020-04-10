
import math
from collections.abc import MutableSequence
from PIL import Image, ImageDraw
from typing import List
from pyrr import Matrix44

from .box import Box
from .filter import Filter

from pyrr import vector, Vector3


def segmentDistance(p: Vector3, v: Vector3, w: Vector3):
    l2 = vector.squared_length(v - w)
    if l2 == 0:
        return vector.length(p - v)

    t = (p - v) | (w - v) / l2
    if t < 0:
        return vector.length(p - v)

    if t > 1:
        return vector.length(p - w)

    return vector.length((v + ((w - v) * t)) - p)


class Path:

    @staticmethod
    def bounding_box(path) -> Box:
        box = Box(path[0], path[0])
        for point in path:
            box = box.extend(Box(point, point))

        return box

    @staticmethod
    def transform(path, matrix: Matrix44):
        result = []
        for v in path:
            result.append(matrix * v)

        return result

    @staticmethod
    def chop(path, step):
        result = []
        for i, a in enumerate(path):
            if i >= len(path) - 1:
                break

            a = Vector3(a)
            b = Vector3(path[i + 1])
            v = b - a
            length = v.length

            if i == 0:
                result.append(a)

            d = step
            while d < length and not math.isclose(d, length):
                result.append(a + (v * (d / length)))
                d += step

            result.append(b)

        return result

    @staticmethod
    def filter(path, f: Filter):
        result = []
        current_path = []
        for v in path:
            v, ok = f.filter(v)
            if ok:
                current_path.append(v)
            else:
                if len(current_path) > 1:
                    result.append(current_path)
                current_path = []

        if len(current_path) > 1:
            result.append(current_path)

        return Paths(result)

    @staticmethod
    def simplify(path, threshold):
        path_length = len(path)

        if path_length < 3:
            return path

        a = Vector3(path[0])
        b = Vector3(path[path_length - 1])
        index = -1
        distance = 0.0

        for i in range(1, path_length - 1):

            p = Vector3(path[i])

            d = segmentDistance(p, a, b)
            if d > distance:
                index = i
                distance = d

        if distance > threshold:
            r1 = Path.simplify(path[:index + 1], threshold)
            r2 = Path.simplify(path[index:], threshold)
            return r1[:len(r1) - 1] + r2
        else:
            return [a, b]

    def to_string(path) -> str:
        result = ""
        for v in path:
            result += "{:f},{:f},{:f};".format(v[0], v[1], v[2])
        return result

    def toSVG(path) -> str:
        coords = []
        for v in path:
            coords.append("{:f},{:f}".format(v[0], v[1]))

        points = " ".join(coords)
        return "<polyline stroke=\"black\" fill=\"none\" points=\"{}\" />".format(points)


class Paths(MutableSequence):
    def __init__(self, paths=None):
        self._paths: List[Path] = paths or []

    def __len__(self):
        return len(self._paths)

    def __getitem__(self, pos):
        return self._paths[pos]

    def __setitem__(self, pos, value: Path):
        self._paths[pos] = value

    def __delitem__(self, pos):
        del self._paths[pos]

    def insert(self, pos, value: Path):
        self._paths.insert(pos, value)

    def bounding_box(self) -> Box:
        box = self._paths[0].bounding_box()
        for path in self._paths:
            box = box.extend(path.bounding_box())

        return box

    def transform(self, matrix: Matrix44):
        return Paths([Path.transform(path, matrix) for path in self._paths])

    def chop(self, step):
        result = []
        for p in self._paths:
            # assert(isinstance(p, Path))
            result.append(Path.chop(p, step))
        # print(result)
        return Paths(result)

    def filter(self, f: Filter):
        result = []
        for path in self._paths:
            # assert(isinstance(path, Path))
            result.extend(Path.filter(path, f)._paths)
        return Paths(result)

    def simplify(self, threshold):
        result = []
        for path in self._paths:
            # assert(isinstance(path, Path))
            result.append(Path.simplify(path, threshold))
        return Paths(result)

    def __str__(self):
        return "\n".join(Path.to_string(path) for path in self._paths)

    def writeToPNG(self, file_path: str, width, height):
        canvas = (width, height)

        im = Image.new('RGBA', canvas, (255, 255, 255, 255))
        draw = ImageDraw.Draw(im)

        for ps in self._paths:
            for i, v1 in enumerate(ps):
                if i >= len(ps) - 1:
                    break
                v2 = ps[i + 1]
                draw.line((v1.x, height - v1.y, v2.x, height - v2.y), fill=0, width=3)

        im.save(file_path)

    def toSVG(self, width, height) -> str:
        lines = []
        lines.append(
            "<svg width=\"{}\" height=\"{}\" version=\"1.1\" baseProfile=\"full\" xmlns=\"http://www.w3.org/2000/svg\">"
            .format(width, height))

        lines.append(
            "<g transform=\"translate(0,{}) scale(1,-1)\">".format(height))
        lines += [Path.toSVG(path) for path in self._paths]
        lines.append("</g></svg>")
        return "\n".join(lines)

    def writeToSVG(self, path: str, width, height):
        with open(path, "w") as file:
            file.write(self.toSVG(width, height))

    def writeToTXT(self, path: str):
        with open(path, "w") as file:
            file.write(str(self))
