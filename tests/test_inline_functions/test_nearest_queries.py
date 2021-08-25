class TestNearestEntityQueries:
    def test_nnear(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        nearest_node = q.nnear(1)
        assert nearest_node in nodes

    def test_knear(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        nearest_keypoint = q.knear(1)
        assert nearest_keypoint in kps

    def test_enearn(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        nearest_element = q.enearn(1)
        assert nearest_element > 0
