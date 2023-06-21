from PySide2 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from qt_material import apply_stylesheet
class PlotWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matplotlib Plot")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.button = QtWidgets.QPushButton("Load Excel File")
        self.button.clicked.connect(self.load_file)
        self.export_button = QtWidgets.QPushButton("Export Plot as PDF")
        self.export_button.clicked.connect(self.export_plot)
        self.export_button.setEnabled(False)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.export_button)
        self.setLayout(self.layout)

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            data = pd.read_excel(file_name)
            x = data["x"]
            y = data["y"]
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, "r-")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title("Line Plot from Excel File")
            self.canvas.draw()
            self.export_button.setEnabled(True)

    def export_plot(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot as PDF", "", "PDF Files (*.pdf)")
        if file_name:
            self.figure.savefig(file_name)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = PlotWindow()
    apply_stylesheet(app, theme='dark_blue.xml')
    window.show()
    app.exec_()