from math import isclose


class TestLineCoordinateQueries:
    def test_lx(self, line_geometry):
        q, kps, line = line_geometry
        x = q.lx(line, 0.5)
        assert x == 0.5

    def test_ly(self, line_geometry):
        q, kps, line = line_geometry
        y = q.ly(line, 0.5)
        assert y == 1.0

    def test_lz(self, line_geometry):
        q, kps, line = line_geometry
        z = q.lz(line, 0.5)
        assert z == 1.0


class TestLineSlopeQueries:
    def test_lsx(self, line_geometry):
        q, kps, line = line_geometry
        sx = q.lsx(line, 0.5)
        actual = 1.0 / 3.0
        assert isclose(sx, actual)

    def test_lsy(self, line_geometry):
        q, kps, line = line_geometry
        sy = q.lsy(line, 0.5)
        actual = 2.0 / 3.0
        assert isclose(sy, actual)

    def test_lsz(self, line_geometry):
        q, kps, line = line_geometry
        sz = q.lsz(line, 0.5)
        actual = 2.0 / 3.0
        assert isclose(sz, actual)
