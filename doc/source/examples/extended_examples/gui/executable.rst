:orphan:

.. _gui_example:

=======================================
Create a GUI app in Python with PySide6
=======================================

This example shows how to create a graphical user interface (GUI) application in Python that use PyMAPDL to compute the deflection of a squared shape beam.

Simulation Configuration
========================

The :download:`gui.py <gui.py>` scripts launch an graphical application using PySide6.
In the preprocessor tab we can enter the `poisson's ratio`, the `Young modulus`, the length of the beam, and the number of point for our simulation.

Add a PyVista plotting frame in our window
==========================================

You can start by importing `QtInteractor` from pyvistaqt and `MapdlTheme` from pymapdl

.. code:: python

    from pyvistaqt import QtInteractor
    from pymapdl import MapdlTheme

We can then add a plotter in the first tab

.. code:: python

    def _setup_tab_preprocessing(self) -> None:
        ...
        container_layout.addWidget(self._run_preprocessor_button, 5, 0, 1, 3)

        # PyVista frame in our window
        self._preprocessing_plotter = QtInteractor(theme=MapdlTheme())
        container_layout.addWidget(self._preprocessing_plotter, 0, 4,
                                   6, 50)

And one in the second tab:

.. code:: python

    def _setup_tab_postprocessing(self) -> None:
        container_layout = QtWidgets.QVBoxLayout()
        self._tab_postprocessing.setLayout(container_layout)
        self._postprocessing_plotter = QtInteractor(theme=MapdlTheme())
        container_layout.addWidget(self._postprocessing_plotter)
        self._deflection_label = QLabel("Deflection: ")
        container_layout.addWidget(self._deflection_label)

Finally we close the widget correctly with the application:

.. code:: python

    def closeEvent(self, event) -> None:
        self._preprocessing_plotter.close()
        self._postprocessing_plotter.close()
        event.accept()  # let the window close


Develop the logic
==============================

In our main section we launch mapdl.

.. code:: python

    from pymapdl import launch_mapdl, Mapdl, MapdlTheme
    ...
    if __name__ == "__main__"
        app = QApplication(sys.argv)
        # Launch mapdl
        mapdl = launch_mapdl()
        window = MainWindow(mapdl)
        window.show()
        sys.exit(app.exec())

For each button we connect it to a function that contains the logic.

.. code:: python

    def _setup_tab_preprocessing(self) -> None:
        ...
        # Button to run the preprocessor
        self._run_preprocessor_button = QPushButton(text="Run preprocessor")
        self._run_preprocessor_button.clicked.connect(self._run_preprocessor)
        ...

    def _setup_tab_solver(self) -> None:
        container_layout = QGridLayout()
        self._tab_solver.setLayout(container_layout)

        self._solve_button = QPushButton(text="Solve")
        self._solve_button.clicked.connect(self._run_solver)

        container_layout.addWidget(self._solve_button)

And write the related functions

.. code:: python
    def _run_preprocessor(self) -> None:
        try:
            poisson_ratio = float(self._poisson_ratio_input.text())
            young_modulus = float(self._young_modulus_input.text())
            length = float(self._length_input.text())
            force = float(self._force_input.text())
        except Exception:
            msgBox = QMessageBox()
            msgBox.setText("Expecting a number")
            msgBox.exec()
            return

        poisson_ratio = float(self._poisson_ratio_input.text())
        young_modulus = float(self._young_modulus_input.text())
        length = float(self._length_input.text())
        force = float(self._force_input.text())

        self._mapdl.clear()
        self._mapdl.verify()
        self._mapdl.prep7()
        self._mapdl.antype("STATIC")
        #create element type
        self._mapdl.et(1, "BEAM188")

        # create material
        self._mapdl.mp("PRXY", 1, poisson_ratio)
        self._mapdl.mp("EX", 1, young_modulus)
        self._mapdl.sectype(1, "BEAM", "RECT")
        self._mapdl.secdata("10", "10")

        self._number_of_nodes = self._number_of_nodes_input.value()

        # create the nodes
        for node_num in range(1, self._number_of_nodes+1):
            self._mapdl.n(node_num,
                          (node_num-1) * length / (self._number_of_nodes-1),
                          0,
                          0)

        # create the elements
        for elem_num in range(1, self._number_of_nodes):
            self._mapdl.e(elem_num, elem_num + 1)

        # fix the extremities of the beam
        self._mapdl.d(1, lab="ALL")
        self._mapdl.d(self._number_of_nodes, lab="ALL")

        #  Apply the force to the node in the middle
        self._mapdl.f(self._number_of_nodes//2 + 1, lab="FY", value=force)

        # Get the pv.Plotter object from mapdl.eplot function
        # to plot in our window
        preprocessing_plotter = self._mapdl.eplot(show_node_numbering=True,
                                                  show_edges=True, cpos="xy",
                                                  return_plotter=True)

        self._preprocessing_plotter.GetRenderWindow().AddRenderer(
            preprocessing_plotter.renderer)

        self._mapdl.finish()

    def _run_solver(self) -> None:
        # solve
        self._mapdl.slashsolu()
        self._mapdl.solve()
        self._mapdl.finish()

        # run postprocessing
        self._mapdl.post1()
        self._mapdl.graphics("power")
        self._mapdl.eshape(1)
        self._mapdl.rgb("index", 100, 100, 100, 0)
        self._mapdl.rgb("index", 0, 0, 0, 15)

        nodal_disp_plotter = self._mapdl.post_processing \
            .plot_nodal_displacement("norm",
                                     show_node_numbering=True, cpos="xy",
                                     return_plotter=True)
        self._postprocessing_plotter.GetRenderWindow().AddRenderer(
            nodal_disp_plotter.renderer)

        mid_node_uy = mapdl.get_value(entity="NODE",
                                      entnum=self._number_of_nodes//2 + 1,
                                      item1="u", it1num="y")
        self._deflection_label.setText(f"Deflection: {mid_node_uy:.3f}")

Additional files
================

You can use this link to download the example file:

* Original :download:`gui.py <gui.py>` script
* Original :download:`gui_app.py <gui_app.py>` script
