import unittest
import math

import ln


class TestRender(unittest.TestCase):
    def test_cube_render(self):
        """
        Test the output of rendering a cube
        """
        scene = ln.Scene()
        scene.add(ln.Cube(ln.Vector3([-1, -1, -1]), ln.Vector3([1, 1, 1])))

        # define camera parameters
        eye = ln.Vector3([4, 3, 2])  # camera position
        center = ln.Vector3([0, 0, 0])  # camera looks at
        up = ln.Vector3([0, 0, 1])  # up direction

        # define rendering parameters
        width = 1024  # rendered width
        height = 1024  # rendered height
        fovy = 50.0  # vertical field of view, degrees
        znear = 0.1  # near z plane
        zfar = 10.0  # far z plane
        step = 0.01  # how finely to chop the paths for visibility testing

        # compute 2D paths that depict the 3D scene
        paths = scene.Render(eye, center, up, width, height,
                             fovy, znear, zfar, step)

        self.assertEqual(len(paths), 9)
        self.assertTrue(math.isclose(paths[0][0].x - 477.218565, 0, abs_tol=0.0001))


if __name__ == '__main__':
    unittest.main()
