class TestFieldComponentValueGetter:
    def test_temp(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(1)
        mapdl.vmesh(1)
        mapdl.d("all", "temp", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        temp_value = mapdl.queries.temp(1)
        assert temp_value == 5.0

    def test_pressure(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(2)
        mapdl.vmesh(1)
        mapdl.d("all", "pres", 5.0)
        mapdl.d("all", "ux", 0.0, lab2="uy", lab3="uz")
        mapdl.slashsolu()
        mapdl.solve()
        pres_value = mapdl.queries.pres(1)
        assert pres_value == 5.0

    def test_volt(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(3)
        mapdl.vmesh(1)
        mapdl.d("all", "volt", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        volt_value = mapdl.queries.volt(1)
        assert volt_value == 5.0

    def test_mag(self, box_with_fields):
        mapdl = box_with_fields
        mapdl.type(4)
        mapdl.vmesh(1)
        mapdl.d("all", "mag", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        mag_value = mapdl.queries.mag(1)
        assert mag_value == 5.0
