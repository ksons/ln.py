import unittest

from ln import Path


class TestPath(unittest.TestCase):
    def test_path_chop(self):
        """
        Test chopping of a path
        """

        path = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
        path = Path.chop(path, 0.1)
        self.assertEqual(len(path), 11)

    def test_path_simplify(self):
        """
        Test simplifying a path
        """

        path = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
        path = Path.chop(path, 0.1)
        self.assertEqual(len(path), 11)
        path1 = Path.simplify(path, 0.1)
        self.assertEqual(len(path1), 2)


if __name__ == '__main__':
    unittest.main()
