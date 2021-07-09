from ansys.mapdl.core.inline_functions import SelectionStatus
import pytest


class TestSelectionStatus:
    @pytest.mark.parametrize('value', [1, -1, 0, 1., -1., 0.])
    def test_happy(self, value):
        select = SelectionStatus(value)
        assert select == value
        assert select is not value

    @pytest.mark.parametrize('value', [1.5, 999, 99., '1'])
    def test_unhappy(self, value):
        with pytest.raises(ValueError):
            SelectionStatus(value)


class TestNSEL:
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.nsel('S', 'LOC', 'X', 0)
        node = q.node(0, 0, 0)
        select = q.nsel(node)
        assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        node = q.node(0, 0, 0)
        q._mapdl.nsel('NONE')
        select = q.nsel(node)
        assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.nsel(999)
        assert select == 0


class TestKSEL:
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.ksel('S', 'LOC', 'X', 0)
        node = q.kp(0, 0, 0)
        select = q.ksel(node)
        assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        node = q.kp(0, 0, 0)
        q._mapdl.ksel('NONE')
        select = q.ksel(node)
        assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.ksel(999)
        assert select == 0


class TestLSEL:
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.lsel('all')
        # there are 6 lines numbered 1-6
        for line in range(1, 7, 1):
            select = q.lsel(line)
            assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.lsel('NONE')
        for line in range(1, 7, 1):
            select = q.lsel(line)
            assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.lsel(999)
        assert select == 0


class TestASEL:
    def test_selected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.asel('all')
        # there are 4 areas numbered 1-4
        for area in range(1, 5, 1):
            select = q.asel(area)
            assert select == 1

    def test_unselected(self, selection_test_geometry):
        q = selection_test_geometry
        q._mapdl.asel('NONE')
        for area in range(1, 5, 1):
            select = q.asel(area)
            assert select == -1

    def test_undefined(self, selection_test_geometry):
        q = selection_test_geometry
        select = q.asel(999)
        assert select == 0
