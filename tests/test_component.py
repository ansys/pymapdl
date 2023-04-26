def test_str_rep(mapdl):
    mapdl.cm("cm1", "nodes")
    assert "cm1" in mapdl.components
    assert "nodes" in mapdl.components


# def test_get_item(mapdl):
#     mapdl.
