# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 10:15:36 2019

@author: ksharma
"""

import geopandas as gp
import numpy as np
import pandas as pd
from shapely.geometry import Point
from scipy.spatial import cKDTree
from collections import defaultdict
from PyQt5 import  QtGui
import pyqtgraph as pg

def load_shape_file(filename):
    return (
        gp.read_file(filename)
        .explode()
        .reset_index()
        .drop(columns=["level_0", "level_1"])
    )


def generate_points(polygon, spacing):
    (minx, miny, maxx, maxy) = polygon.bounds
    x_coords = np.arange(
        np.floor(minx), (np.ceil(maxx)), spacing
    )
    y_coords = np.arange(
        np.floor(miny), (np.ceil(maxy)), spacing
    )
    grid_x, grid_y = map(
        np.ndarray.flatten, np.meshgrid(x_coords, y_coords)
    )
    grid = gp.GeoSeries(
        [Point(x, y) for x, y in zip(grid_x, grid_y)]
    )
    return grid[grid.intersects(polygon)].reset_index(
        drop=True
    )


def random_population(size, ratio):
    samples = np.zeros(size, dtype=np.bool)
    samples[: round(size * ratio)] = 1
    return np.random.permutation(samples)


def populate_simulation(
    *,
    shape_file: gp.GeoDataFrame,
    spacing: float,
    empty_ratio: float,
    demographic_ratio: float,
    races=2,
    random_seed=None,
):

    if random_seed is not None:
        np.random.seed(random_seed)
    all_houses = pd.concat(
        [
            generate_points(polygon, spacing)
            for polygon in shape_file.geometry
        ],
        ignore_index=True,
    )
    occupied = random_population(
        size=len(all_houses), ratio=1 - empty_ratio
    )
    race = random_population(
        size=int(occupied.sum()), ratio=1 - demographic_ratio
    )

    agent_houses = gp.GeoDataFrame(
        {"Race": race.astype(int)},
        geometry=all_houses[occupied].reset_index(
            drop=True
        ),
    )
    empty_houses = all_houses[~occupied].reset_index(
        drop=True
    )
    
    return empty_houses, agent_houses


class Update:
    def __init__(
        self,
        agent_houses,
        empty_houses,
        spacing,
        iterations,
        similarity_threshold,
        shape_file,
        p,
        geometry
    ):
        
        self.agent_houses = agent_houses
        self.empty_houses = empty_houses
        self.spacing = spacing
        self.iterations = iterations
        self.similarity_threshold = similarity_threshold
        self.shape_file = shape_file
        self.p = p
        self.geometry = geometry
        self.kill = False
    def is_unsatisfied(
        self, agent, all_neighbours, race_list
    ):
        neighbours_indices = all_neighbours[agent]
        race = race_list[agent]
        neighbours = race_list[neighbours_indices]
        if len(neighbours) == 0:
            return False
        else:
            return (
                len(neighbours[neighbours == race])
                / len(neighbours)
                < self.similarity_threshold
            )

    def move(self, agent, *, race):
        x, y = agent[0], agent[1]
        (x_new, y_new) = self.empty_houses[
            np.random.choice(self.empty_houses.shape[0], 1),
            :,
        ][0]
        self.agent_houses = self.agent_houses[~np.isclose(self.agent_houses,np.array([race,x,y])).all(axis=1)]
       
        self.agent_houses = np.vstack(
            [self.agent_houses, [race, x_new, y_new]]
        )
        self.empty_houses = self.empty_houses[~np.isclose(self.empty_houses,np.array([x_new, y_new])).all(axis=1)]
        
        self.empty_houses = np.vstack(
            [self.empty_houses, [x, y]]
        )

    def update_helper(
        self, index, all_neighbours, race_list, agent_houses
    ):
        if self.is_unsatisfied(
            index, all_neighbours, race_list
        ):
            self.move(
                agent_houses[index], race=race_list[index]
            )
            return 1
        else:
            return 0

    def update(self):
        for iterations in np.arange(self.iterations):
            old_agent_houses = self.agent_houses[
                :, [1, 2]
            ].copy()
            race = self.agent_houses[:, 0].copy()
            all_neighbours = defaultdict(list)
            tree = cKDTree(old_agent_houses)
            for i, j in tree.query_pairs(self.spacing * 2):
                all_neighbours[i].append(j)
                all_neighbours[j].append(i)
            changes = 0
            for index in np.arange(len(old_agent_houses)):
                changes += self.update_helper(
                    index,
                    all_neighbours,
                    race,
                    old_agent_houses,
                )
          
            self.p.scatterPlot(self.agent_houses[:, 1],
                self.agent_houses[:, 2],
                brush=[
                    pg.mkBrush(v)
                    for v in np.where(
                        self.agent_houses[:, 0] == 0.0,
                        "w",
                        "y",
                    )
                ],clear=True)
            for i in self.geometry:
                self.p.plot(i[:, 0], i[:, 1], pen=pg.mkPen( width=3))
            
            QtGui.QApplication.processEvents()
            if self.kill:
                break
            if changes == 0:
                break
            print("n Changes---->" + str(changes))
            print("Majority Agents Number ----> " + str(len(self.agent_houses[:,0][self.agent_houses[:,0]==0])))
            print("Minority Agents Number ----> " + str(len(self.agent_houses[:,0][self.agent_houses[:,0]==1])))            