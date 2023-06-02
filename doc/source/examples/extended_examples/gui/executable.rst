:orphan:

.. _gui_example:

=======================================
Create a GUI app in Python with PySide6
=======================================

This example shows how to create a graphical user interface (GUI) app in Python that use PyMAPDL to compute the deflection of a squared shape beam.

Simulation configuration
========================

The :download:`gui.py <gui.py>` scripts launch an graphical app using PySide6.
In the preprocessing tab, there is a field for the poisson's ratio, the Young modulus, the length of the beam, and the number of point for the simulation.

Add a PyVista plotting frame in the window
==========================================

Start by importing `QtInteractor` from pyvistaqt and `MapdlTheme` from PyMAPDL

.. code:: python

    from pyvistaqt import QtInteractor
    from pymapdl import MapdlTheme

Then add a plotter in the first tab

.. code:: python

    def _setup_tab_preprocessing(self) -> None:
        ...
        container_layout.addWidget(self._run_preprocessor_button, 5, 0, 1, 3)

        # PyVista frame in the window
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

Finally, close the widget correctly with the app:

.. code:: python

    def closeEvent(self, event) -> None:
        self._preprocessing_plotter.close()
        self._postprocessing_plotter.close()
        event.accept()  # let the window close


Develop the logic
==============================

In the main section, launch MAPDL.

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

Connect each button to a function that contains the logic.

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

.. literalinclude:: gui_app.py
    :start-line: 124
    :end-line: 210

Additional files
================

You can use this link to download the example file:

* Original :download:`gui.py <gui.py>` script
* Original :download:`gui_app.py <gui_app.py>` script
