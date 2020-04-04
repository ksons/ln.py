import unittest

import ln


class TestPath(unittest.TestCase):
    def test_path_chop(self):
        """
        Test chopping of a path
        """

        path = ln.Path([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        path = path.chop(0.1)
        self.assertEqual(len(path), 11)
        path = path.simplify(0.1)

    def test_path_simplify(self):
        """
        Test simplifying a path
        """

        path = ln.Path([ln.Vector3([0.0, 0.0, 0.0]), ln.Vector3([0.0, 0.0, 1.0])])
        path = path.chop(0.1)
        self.assertEqual(len(path), 11)
        path1 = path.simplify(0.1)
        self.assertEqual(len(path1), 2)


if __name__ == '__main__':
    unittest.main()
