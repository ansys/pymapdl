from PySide6.QtCore import Qt
from ansys.mapdl.core import launch_mapdl, Mapdl, MapdlTheme
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                               QLineEdit, QPushButton, QSlider, QLabel,
                               QGridLayout, QMessageBox)
from PySide6.QtGui import QIntValidator
from PySide6 import QtWidgets
from pyvistaqt import QtInteractor
import sys


class MainWindow(QMainWindow):
    def __init__(self, mapdl: Mapdl, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._mapdl = mapdl

    def _setup_ui(self) -> None:
        self.setWindowTitle("pyMAPDL example application")
        self.resize(1000, 500)
        self._widget = QWidget()
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._tab_widget = QtWidgets.QTabWidget()

        self._tab_preprocessing = QtWidgets.QWidget()
        self._tab_widget.addTab(self._tab_preprocessing, "Preprocessing")
        self._setup_tab_preprocessing()

        self._tab_solver = QtWidgets.QWidget()
        self._tab_widget.addTab(self._tab_solver, "Solver")
        self._setup_tab_solver()

        self._tab_postprocessing = QtWidgets.QWidget()
        self._tab_widget.addTab(self._tab_postprocessing, "Postprocessing")
        self._setup_tab_postprocessing()

        self._layout.addWidget(self._tab_widget)
        self._widget.setLayout(self._layout)
        self.setCentralWidget(self._widget)

    def _setup_tab_preprocessing(self) -> None:
        container_layout = QGridLayout()
        max_qlineedit_width = 250
        self._tab_preprocessing.setLayout(container_layout)

        poisson_ratio_label = QLabel("Poisson's ratio: ")
        container_layout.addWidget(poisson_ratio_label, 0, 0)
        self._poisson_ratio_input = QLineEdit()
        self._poisson_ratio_input.setPlaceholderText("Poisson's ratio (PRXY)")
        self._poisson_ratio_input.setValidator(QIntValidator())
        self._poisson_ratio_input.setText("0.3")
        self._poisson_ratio_input.setMaximumWidth(max_qlineedit_width)

        young_modulus_label = QLabel("Young's modulus: ")
        container_layout.addWidget(young_modulus_label, 1, 0)
        self._young_modulus_input = QLineEdit()
        self._young_modulus_input.setPlaceholderText(
            "Young's modulus in the x direction")
        self._young_modulus_input.setValidator(QIntValidator())
        self._young_modulus_input.setText("210e3")
        self._young_modulus_input.setMaximumWidth(max_qlineedit_width)

        length_label = QLabel("Length: ")
        container_layout.addWidget(length_label, 2, 0)
        self._length_input = QLineEdit()
        self._length_input.setPlaceholderText("Length")
        self._length_input.setValidator(QIntValidator())
        self._length_input.setMaximumWidth(max_qlineedit_width)

        force_label = QLabel("Force: ")
        container_layout.addWidget(force_label, 3, 0)
        self._force_input = QLineEdit()
        self._force_input.setPlaceholderText("Load force")
        self._force_input.setMaximumWidth(max_qlineedit_width)

        number_of_nodes_label = QLabel("Number of nodes: ")
        container_layout.addWidget(number_of_nodes_label, 4, 0)
        self._number_of_nodes_input = QSlider(
            orientation=Qt.Orientation.Horizontal)
        self._number_of_nodes_input.setMinimum(3)
        self._number_of_nodes_input.setMaximum(9)
        self._number_of_nodes_input.setValue(5)
        self._number_of_nodes_input.setSingleStep(2)
        self._number_of_nodes_input.setPageStep(2)
        self._number_of_nodes_input.setMaximumWidth(max_qlineedit_width-50)
        self._number_of_node_label = QLabel(
            f"{self._number_of_nodes_input.value()} nodes")
        self._number_of_nodes_input.valueChanged.connect(
            lambda _: self._number_of_node_label.setText(
                f"{self._number_of_nodes_input.value()} nodes"))

        # Button to run the preprocessor
        self._run_preprocessor_button = QPushButton(text="Run preprocessor")
        self._run_preprocessor_button.clicked.connect(self._run_preprocessor)

        container_layout.addWidget(self._poisson_ratio_input, 0, 1, 1, 2)
        container_layout.addWidget(self._young_modulus_input, 1, 1, 1, 2)
        container_layout.addWidget(self._length_input, 2, 1, 1, 2)
        container_layout.addWidget(self._force_input, 3, 1, 1, 2)
        container_layout.addWidget(self._number_of_nodes_input, 4, 1, 1, 1)
        container_layout.addWidget(self._number_of_node_label, 4, 2, 1, 1)
        container_layout.addWidget(self._run_preprocessor_button, 5, 0, 1, 3)

        # PyVista frame in our window
        self._preprocessing_plotter = QtInteractor(theme=MapdlTheme())
        container_layout.addWidget(self._preprocessing_plotter, 0, 4,
                                   6, 50)

    def _setup_tab_solver(self) -> None:
        container_layout = QGridLayout()
        self._tab_solver.setLayout(container_layout)

        self._solve_button = QPushButton(text="Solve")
        self._solve_button.clicked.connect(self._run_solver)

        container_layout.addWidget(self._solve_button)

    def _setup_tab_postprocessing(self) -> None:
        container_layout = QtWidgets.QVBoxLayout()
        self._tab_postprocessing.setLayout(container_layout)
        self._postprocessing_plotter = QtInteractor(theme=MapdlTheme())
        container_layout.addWidget(self._postprocessing_plotter)
        self._deflection_label = QLabel("Deflection: ")
        container_layout.addWidget(self._deflection_label)

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
        self._mapdl.slashsolu()
        self._mapdl.solve()
        self._mapdl.finish()
        self._run_post_processor()

    def _run_post_processor(self) -> None:
        self._mapdl.post1()
        self._mapdl.graphics("power")
        self._mapdl.eshape(1)
        self._mapdl.rgb("index", 100, 100, 100, 0)
        self._mapdl.rgb("index", 0, 0, 0, 15)

        mapdl.upcoord(2)

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

    def closeEvent(self, event) -> None:
        self._preprocessing_plotter.close()
        self._postprocessing_plotter.close()
        event.accept()  # let the window close


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mapdl = launch_mapdl()
    window = MainWindow(mapdl)
    window.show()
    sys.exit(app.exec())
