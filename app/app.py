# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 20:09:53 2019

@author: karti
"""

from PyQt5 import QtWidgets, uic, QtCore
import pyqtgraph as pg
from app.geoschelling import *
import numpy as np
import sys

class App(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        uic.loadUi(
            "app/res/schelling.ui",    
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

        self.shapefilepath = "./app/State_Shapefiles/AK/AK.shp"
        self.spacing = 0.1
        self.empty_ratio = 0.1
        self.demographic_ratio = 0.01
        self.similarity_threshold = 0.01
        self.update_geo = None
        self.spacingLabel.setText(str(self.spacing))
        self.emptyLabel.setText(str(self.empty_ratio))
        self.similarityLabel.setText(str(self.similarity_threshold))
        self.demographicLabel.setText(str(self.demographic_ratio))

        self.populateButton.clicked.connect(self.populate)
        self.runButton.clicked.connect(self.update)
        self.endButton.clicked.connect(self.kill)
        self.spacingSlider.valueChanged.connect(
            self.set_spacing
        )
        self.emptyratioSlider.valueChanged.connect(
            self.set_empty_ratio
        )
        self.demographicSlider.valueChanged.connect(
            self.set_demographic_ratio
        )
        self.similaritySlider.valueChanged.connect(
            self.set_similarity_threshold
        )
        self.comboBox.addItems(state_names)
        self.comboBox.activated.connect(self.set_filepath)

    def set_spacing(self):
        self.spacing = self.spacingSlider.value() / 100
        self.spacingLabel.setText(str(self.spacing))
        print(self.spacing)

    def set_empty_ratio(self):
        self.empty_ratio = (
            self.emptyratioSlider.value() / 10
        )
        self.emptyLabel.setText(str(self.empty_ratio))
        print(self.empty_ratio)
        
    def set_similarity_threshold(self):
        self.similarity_threshold = (
            self.similaritySlider.value() / 100
        )
        self.similarityLabel.setText(str(self.similarity_threshold))
        print(self.similarity_threshold)

    def set_demographic_ratio(self):
        self.demographic_ratio = (
            self.demographicSlider.value() / 100
        )
        self.demographicLabel.setText(str(self.demographic_ratio))
        print(self.demographic_ratio)

    def set_filepath(self):
        self.shapefilepath = "./app/State_Shapefiles/{}/{}.shp".format(
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
          

    def update(self):
        self.update_geo = Update(
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
        self.update_geo.update()
    
    def kill(self):
        if self.update_geo is not None:
            self.update_geo.kill = True