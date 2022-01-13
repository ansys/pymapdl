class TestFieldComponentValueGetter:
    def build_setup(self, mapdl):
        mapdl.prep7()
        mapdl.mp("kxx", 1, 45)
        mapdl.mp("ex", 1, 2e10)
        mapdl.mp("perx", 1, 1)
        mapdl.mp("murx", 1, 1)
        mapdl.et(1, 'SOLID70')
        mapdl.et(2, 'CPT215')
        mapdl.et(3, 'SOLID122')
        mapdl.et(4, 'SOLID96')
        mapdl.block(0, 1, 0, 1, 0, 1)
        mapdl.esize(0.5)

    def test_temp(self, mapdl):
        self.build_setup(mapdl)
        mapdl.type(1)
        mapdl.vmesh(1)
        mapdl.d("all", "temp", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        temp_value = mapdl.queries.temp(1)
        assert temp_value is not None

    def test_pressure(self, mapdl):
        self.build_setup(mapdl)
        mapdl.type(2)
        mapdl.vmesh(1)
        mapdl.d("all", "pres", 5.0)
        mapdl.d("all", "ux", 0.0, lab2="uy", lab3="uz")
        mapdl.slashsolu()
        mapdl.solve()
        pres_value = mapdl.queries.pres(1)
        assert pres_value is not None

    def test_volt(self, mapdl):
        self.build_setup(mapdl)
        mapdl.type(3)
        mapdl.vmesh(1)
        mapdl.d("all", "volt", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        volt_value = mapdl.queries.volt(1)
        assert volt_value is not None

    def test_mag(self, mapdl):
        self.build_setup(mapdl)
        mapdl.type(4)
        mapdl.vmesh(1)
        mapdl.d("all", "mag", 5.0)
        mapdl.slashsolu()
        mapdl.solve()
        mag_value = mapdl.queries.mag(1)
        assert mag_value is not None
