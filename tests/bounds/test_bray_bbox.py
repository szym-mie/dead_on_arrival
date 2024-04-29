import unittest

from pyglet.math import Vec2

from src.bounds.bbox import BBox
from src.bounds.bray import BRay
from tests.run_test import run_test


@run_test
class TestBRayBBox(unittest.TestCase):
    def test_intersect(self):
        ray = BRay(Vec2(0, 0), Vec2(4, 1))
        box = BBox(Vec2(2, -2), Vec2(2, 4))

        self.assertTrue(ray.test_bbox(box))

    def test_not_intersect(self):
        ray = BRay(Vec2(0, 0), Vec2(2, 3))
        box = BBox(Vec2(2, -2), Vec2(4, 2))

        self.assertFalse(ray.test_bbox(box))
