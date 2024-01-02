class TestNormalsNodeQueries:
    @staticmethod
    def build_plane(mapdl, plane: str):
        n1 = mapdl.n(1, 0, 0, 0)
        if plane == "xy":
            n2 = mapdl.n(2, 0, 1, 0)
            n3 = mapdl.n(3, 1, 1, 0)
        elif plane == "xz":
            n2 = mapdl.n(2, 1, 0, 0)
            n3 = mapdl.n(3, 1, 0, 1)
        elif plane == "yz":
            n2 = mapdl.n(2, 0, 1, 0)
            n3 = mapdl.n(3, 0, 1, 1)
        return n1, n2, n3

    def test_normnx(self, query):
        nodes = self.build_plane(query._mapdl, "yz")
        cosine = query.normnx(*nodes)
        assert abs(cosine) == 1.0

    def test_normny(self, query):
        nodes = self.build_plane(query._mapdl, "xz")
        cosine = query.normny(*nodes)
        assert abs(cosine) == 1.0

    def test_normnz(self, query):
        nodes = self.build_plane(query._mapdl, "xy")
        cosine = query.normnz(*nodes)
        assert abs(cosine) == 1.0


class TestNormalsKeypointsQueries:
    @staticmethod
    def build_plane(mapdl, plane: str):
        k1 = mapdl.k(1, 0, 0, 0)
        if plane == "xy":
            k2 = mapdl.k(2, 0, 1, 0)
            k3 = mapdl.k(3, 1, 1, 0)
        elif plane == "xz":
            k2 = mapdl.k(2, 1, 0, 0)
            k3 = mapdl.k(3, 1, 0, 1)
        elif plane == "yz":
            k2 = mapdl.k(2, 0, 1, 0)
            k3 = mapdl.k(3, 0, 1, 1)
        return k1, k2, k3

    def test_normkx(self, query):
        keypoints = self.build_plane(query._mapdl, "yz")
        cosine = query.normkx(*keypoints)
        assert abs(cosine) == 1.0

    def test_normky(self, query):
        keypoints = self.build_plane(query._mapdl, "xz")
        cosine = query.normky(*keypoints)
        assert abs(cosine) == 1.0

    def test_normkz(self, query):
        keypoints = self.build_plane(query._mapdl, "xy")
        cosine = query.normkz(*keypoints)
        assert abs(cosine) == 1.0
