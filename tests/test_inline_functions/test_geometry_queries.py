import pytest
from collections import namedtuple
from math import pi, isclose
from itertools import combinations

PointTrioAngle = namedtuple('PointTrioAngle', ['point1', 'point2', 'vertex', 'angle'])
Triangle = namedtuple('Triangle', ['point1', 'point2', 'point3', 'area'])

angles = [PointTrioAngle((1, 0, 0), (0, 1, 0), (0, 0, 0), pi*.5),
          PointTrioAngle((1, 0, 0), (0, 0, 1), (0, 0, 0), pi*.5),
          PointTrioAngle((0, 0, 1), (0, 1, 0), (0, 0, 0), pi*.5),
          PointTrioAngle((1, 1, 0), (0, 1, 0), (0, 0, 0), pi*.25),
          PointTrioAngle((1, 1, 1), (0, 0, 0), (0, 0, 0), 0.),
          PointTrioAngle((1, 1, 1), (1, 1, 1), (0, 0, 0), 0.),
          PointTrioAngle((1, 0, 0), (-1, 0, 0), (0, 0, 0), pi),
          PointTrioAngle((1, 0, 0), (-1, -1, 0), (0, 0, 0), pi*.75),
          PointTrioAngle((0, 0, 0), (0, 0, 0), (0, 0, 0), 0.)]

triangles = [Triangle((1, 0, 0), (0, 0, 0), (0, 1, 0), 0.5),
             Triangle((1, 0, 0), (0, 0, 0), (0, .5, 0), 0.25),
             Triangle((1, 0, 0), (0, 0, 0), (1, 0, 0), 0.),
             Triangle((0, 0, 0), (0, 0, 0), (0, 0, 0), 0.),
             Triangle((1, 0, 0), (-1, 0, 0), (0, 1, 0), 1.0),
             Triangle((1, 0, 0), (0, 0, 0), (0, 1, 0), 0.5),
             Triangle((1, 0, 0), (0, 1, 0), (0, 0, 1), 0.8660254038)]


class TestAngleQueries:
    @pytest.mark.parametrize('coords', angles)
    def test_anglen(self, query, mapdl, cleared, coords: PointTrioAngle):
        n1 = mapdl.n(1, *coords.vertex)
        n2 = mapdl.n(2, *coords.point1)
        n3 = mapdl.n(3, *coords.point2)
        assert isclose(query.anglen(n1, n2, n3), coords.angle)

    @pytest.mark.parametrize('coords', angles)
    def test_anglek(self, query, mapdl, cleared, coords: PointTrioAngle):
        k1 = mapdl.k(1, *coords.vertex)
        k2 = mapdl.k(2, *coords.point1)
        k3 = mapdl.k(3, *coords.point2)
        assert isclose(query.anglek(k1, k2, k3), coords.angle)


class TestTriangleAreaQueries:
    def test_areand_order_invariant(self, mapdl, cleared):
        triangle = Triangle((1, 0, 0), (0, 1, 0), (0, 0, 1), 0.8660254038)
        n1 = mapdl.n(1, *triangle.point1)
        n2 = mapdl.n(2, *triangle.point2)
        n3 = mapdl.n(3, *triangle.point3)
        for combo in combinations([n1, n2, n3], 3):
            area = mapdl.queries.areand(*combo)
            print(combo)
            assert isclose(area, triangle.area)

    @pytest.mark.parametrize('triangle', triangles)
    def test_areand_various_triangles(self, mapdl, cleared, triangle: Triangle):
        n1 = mapdl.n(1, *triangle.point1)
        n2 = mapdl.n(2, *triangle.point2)
        n3 = mapdl.n(3, *triangle.point3)
        area = mapdl.queries.areand(n1, n2, n3)
        assert isclose(area, triangle.area)

    def test_areakp_order_invariant(self, mapdl, cleared):
        triangle = Triangle((1, 0, 0), (0, 1, 0), (0, 0, 1), 0.8660254038)
        k1 = mapdl.k(1, *triangle.point1)
        k2 = mapdl.k(2, *triangle.point2)
        k3 = mapdl.k(3, *triangle.point3)
        for combo in combinations([k1, k2, k3], 3):
            area = mapdl.queries.areakp(*combo)
            assert isclose(area, triangle.area)

    @pytest.mark.parametrize('triangle', triangles)
    def test_areakp_various_triangles(self, mapdl, cleared, triangle: Triangle):
        k1 = mapdl.k(1, *triangle.point1)
        k2 = mapdl.k(2, *triangle.point2)
        k3 = mapdl.k(3, *triangle.point3)
        area = mapdl.queries.areakp(k1, k2, k3)
        assert isclose(area, triangle.area)
