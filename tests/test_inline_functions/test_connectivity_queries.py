class TestConnectivityQueries:
    def test_nelem(self, box_geometry):
        q, kps, areas, nodes = box_geometry
        ns = [q.nelem(1, i) for i in range(1, 21)]
        for n in ns:
            assert n in nodes or n == 0

    def test_enextn(self, box_geometry, common_functions_and_classes):
        _, get_details_of_elements, _, _ = common_functions_and_classes
        q, kps, areas, nodes = box_geometry
        es = [q.enextn(n, 1) for n in nodes]
        for e in es:
            assert e > 0
