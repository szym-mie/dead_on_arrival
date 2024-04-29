from __future__ import annotations
from math import sqrt, inf

from pyglet.math import Vec2

from src.bounds.btester import BTester


class BRay(BTester):
    def __init__(self, start: Vec2, leader: Vec2):
        self.start = start
        self.leader = leader

        sx = self.start.x
        sy = self.start.y
        lx = self.leader.x
        ly = self.leader.y
        dy = ly - sy
        dx = lx - sx

        self.normal = (leader - start).normalize()
        self.normal_inv = None
        self.update_normal_inv()

        self.a = dy
        self.b = dx
        self.c = sy * dx + sx * dy

    def update_normal_inv(self):
        try:
            inx = 1 / self.normal.x
        except ZeroDivisionError:
            inx = inf * self.normal.x

        try:
            iny = 1 / self.normal.y
        except ZeroDivisionError:
            iny = inf * self.normal.y

        self.normal_inv = Vec2(inx, iny)

    def _distance_to_point(self, vec: Vec2) -> float:
        p = abs(self.a * vec.x + self.b * vec.y + self.c)
        m = sqrt(self.a * self.a + self.b * self.b)
        return p / m

    def _is_point_in_quarter(self, vec: Vec2) -> bool:
        vec_offset = vec - self.start
        gx = self.normal.x
        gy = self.normal.y
        ox = vec_offset.x
        oy = vec_offset.y
        x_aligned = (gx > 0 and ox > 0) or (gx < 0 and ox < 0)
        y_aligned = (gy > 0 and oy > 0) or (gy < 0 and oy < 0)
        return x_aligned and y_aligned

    def test_point(self, vec) -> Vec2 | None:
        e = 0.00001
        if self._is_point_in_quarter(vec) and self._distance_to_point(vec) < e:
            return vec
        return None

    def test_bray(self, other) -> Vec2 | None:
        return None

    def test_bbox(self, other) -> Vec2 | None:
        sx = self.start.x
        sy = self.start.y
        inx = self.normal_inv.x
        iny = self.normal_inv.y

        tx1 = (other.lower.x - sx) * inx
        tx2 = (other.upper.x - sx) * inx

        t_min = min(tx1, tx2)
        t_max = max(tx1, tx2)

        ty1 = (other.lower.y - sy) * iny
        ty2 = (other.upper.y - sy) * iny

        t_min = max(t_min, min(ty1, ty2))
        t_max = min(t_max, max(ty1, ty2))

        if t_max >= t_min:
            return self.start + self.normal * t_min
        return None

    def test_bcircle(self, other) -> Vec2 | None:
        d = self._distance_to_point(other.center)
        if d < other.radius:
            pass
            # cad = other.center.distance(vec_a)
            # cbd = other.center.distance(vec_b)
        return None
