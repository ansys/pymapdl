from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                               QLineEdit, QPushButton, QSlider, QLabel,
                               QGridLayout)
from PySide6 import QtWidgets
import sys


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._setup_ui()

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
        self._poisson_ratio_input.setText("0.3")
        self._poisson_ratio_input.setMaximumWidth(max_qlineedit_width)

        young_modulus_label = QLabel("Young's modulus: ")
        container_layout.addWidget(young_modulus_label, 1, 0)
        self._young_modulus_input = QLineEdit()
        self._young_modulus_input.setPlaceholderText(
            "Young's modulus in the x direction")
        self._young_modulus_input.setText("210e3")
        self._young_modulus_input.setMaximumWidth(max_qlineedit_width)

        length_label = QLabel("Length: ")
        container_layout.addWidget(length_label, 2, 0)
        self._length_input = QLineEdit()
        self._length_input.setPlaceholderText("Length")
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

        container_layout.addWidget(self._poisson_ratio_input, 0, 1, 1, 2)
        container_layout.addWidget(self._young_modulus_input, 1, 1, 1, 2)
        container_layout.addWidget(self._length_input, 2, 1, 1, 2)
        container_layout.addWidget(self._force_input, 3, 1, 1, 2)
        container_layout.addWidget(self._number_of_nodes_input, 4, 1, 1, 1)
        container_layout.addWidget(self._number_of_node_label, 4, 2, 1, 1)
        container_layout.addWidget(self._run_preprocessor_button, 5, 0, 1, 3)

    def _setup_tab_solver(self) -> None:
        container_layout = QGridLayout()
        self._tab_solver.setLayout(container_layout)

        self._solve_button = QPushButton(text="Solve")

        container_layout.addWidget(self._solve_button)

    def _setup_tab_postprocessing(self) -> None:
        container_layout = QtWidgets.QVBoxLayout()
        self._tab_postprocessing.setLayout(container_layout)
        self._deflection_label = QLabel("Deflection: ")
        container_layout.addWidget(self._deflection_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
