# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 20:09:53 2019

@author: karti
"""

from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
from geoschelling import *
import numpy as np
import sys

class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        uic.loadUi(
            "res/schelling.ui",    
            self
        )

        state_names = [
            "AK",
            "AL",
            "AR",
            "AZ",
            "CA",
            "CO",
            "CT",
            "DC",
            "DE",
            "FL",
            "GA",
            "HI",
            "IA",
            "ID",
            "IL",
            "IN",
            "KS",
            "KY",
            "LA",
            "MA",
            "MD",
            "ME",
            "MI",
            "MN",
            "MO",
            "MS",
            "MT",
            "NC",
            "ND",
            "NE",
            "NH",
            "NJ",
            "NM",
            "NV",
            "NY",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VA",
            "VT",
            "WA",
            "WI",
            "WV",
            "WY",
        ]

        self.shapefilepath = "./State_Shapefiles/AK/AK.shp"
        self.spacing = 0.1
        self.empty_ratio = 0.1
        self.demographic_ratio = 0.01
        self.similarity_threshold = 0.01

        self.label_6.setText(str(self.spacing))
        self.label_7.setText(str(self.empty_ratio))
        self.label_8.setText(str(self.similarity_threshold))
        self.label_9.setText(str(self.demographic_ratio))

        self.pushButton_3.clicked.connect(self.populate)
        self.pushButton.clicked.connect(self.update)
        self.horizontalSlider.valueChanged.connect(
            self.set_spacing
        )
        self.horizontalSlider_2.valueChanged.connect(
            self.set_empty_ratio
        )
        self.horizontalSlider_4.valueChanged.connect(
            self.set_demographic_ratio
        )
        self.horizontalSlider_3.valueChanged.connect(
            self.set_similarity_threshold
        )
        self.comboBox.addItems(state_names)
        self.comboBox.activated.connect(self.set_filepath)

    def set_spacing(self):
        self.spacing = self.horizontalSlider.value() / 100
        self.label_6.setText(str(self.spacing))
        print(self.spacing)

    def set_empty_ratio(self):
        self.empty_ratio = (
            self.horizontalSlider_2.value() / 10
        )
        self.label_7.setText(str(self.empty_ratio))
        print(self.empty_ratio)

    def set_demographic_ratio(self):
        self.demographic_ratio = (
            self.horizontalSlider_4.value() / 100
        )
        self.label_9.setText(str(self.demographic_ratio))
        print(self.demographic_ratio)

    def set_similarity_threshold(self):
        self.similarity_threshold = (
            self.horizontalSlider_3.value() / 100
        )
        self.label_8.setText(str(self.similarity_threshold))
        print(self.similarity_threshold)

    def set_filepath(self):
        self.shapefilepath = "./State_Shapefiles/{}/{}.shp".format(
            str(self.comboBox.currentText()),
            str(self.comboBox.currentText()),
        )

    def populate(self):
        self.shape_file = load_shape_file(
            self.shapefilepath
        )

        empty_houses, agent_houses = populate_simulation(
            shape_file=self.shape_file,
            spacing=self.spacing,
            empty_ratio=self.empty_ratio,
            demographic_ratio=self.demographic_ratio,
            races=2,
            random_seed=0,
        )

        self.agent_houses = np.array(
            [
                agent_houses.Race,
                agent_houses.geometry.x,
                agent_houses.geometry.y,
            ]
        ).T
        self.empty_houses = np.array(
            [
                empty_houses.geometry.x,
                empty_houses.geometry.y,
            ]
        ).T


        self.geometry = list(
            self.shape_file.geometry.apply(
                lambda x: np.array(x.exterior.coords[:-1])
            )
        )
        self.win = pg.GraphicsWindow(title="Simulation")
        self.win.setGeometry(0, 100, 1000, 600)

        self.p = self.win.addPlot()
        self.p.hideAxis("left")
        self.p.hideAxis("bottom")
        for i in self.geometry:
            self.p.plot(i[:, 0], i[:, 1],pen=pg.mkPen( width=3))
            
        self.p.scatterPlot(self.agent_houses[:, 1],
            self.agent_houses[:, 2],
            brush=[
                pg.mkBrush(v)
                for v in np.where(
                    self.agent_houses[:, 0] == 0.0, "w", "y"
                )
            ],
        )
          
        style1 = pg.PlotDataItem(
            pen=pg.mkPen(None), symbol="o",brush=pg.mkBrush(255, 255, 255, 20), symbolBrush=pg.mkBrush(255, 255, 255, 20)
        )
        style2 = pg.PlotDataItem(
            pen=pg.mkPen(None), symbol="o", brush=pg.mkBrush(255, 255, 255, 20),symbolBrush=pg.mkBrush(255, 255, 255, 20)
        )
        legend = self.p.addLegend()
        legend.addItem(style2, " Majority")
        legend.addItem(style1, " Minority")

    def update(self):
        update_geo = Update(
            self.agent_houses,
            self.empty_houses,
            self.spacing,
            500,
            self.similarity_threshold,
            self.shape_file,
            self.p,
            self.geometry
        )
        self.p.scatterPlot(clear=True)
        update_geo.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    # app.setWindowIcon(QtGui.QIcon(ex.resource_path("resources\pdf-to-excel-icon.png")))
    ex.show()
    app.exec_()