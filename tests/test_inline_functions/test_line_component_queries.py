

class TestLineCoordinateQueries:
    def test_lx(self, line_geometry):
        q, kps, line = line_geometry
        x = q.lx(line, 0.5)
        assert x == 0.5

    def test_ly(self, line_geometry):
        q, kps, line = line_geometry
        y = q.ly(line, 0.5)
        assert y == 0.5

    def test_lz(self, line_geometry):
        q, kps, line = line_geometry
        z = q.lz(line, 0.5)
        assert z == 0.5
