from app import App
import sys
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    # app.setWindowIcon(QtGui.QIcon(ex.resource_path("resources\example.png")))
    ex.show()
    app.exec_()