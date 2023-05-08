def test_str_rep(mapdl, cleared):
    assert len(mapdl.component.__str__().splitlines()) == 2
    mapdl.cm("cm1", "nodes")
    assert "cm1" in mapdl.components
    assert "nodes" in mapdl.components
    assert len(mapdl.component.__str__().splitlines()) == 3


def test_set_item(mapdl, cleared):
    mapdl.component["mycomp"] = "node", [1, 2, 3]
