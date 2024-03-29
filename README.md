# Geo-schelling
Geo-schelling is an app built with PyQt5 and PyQtGraph to run the simulation of Schelling's Model of Segregation on a geographical map.

![Screenshot](https://github.com/kartikeyas00/geo-schelling/blob/master/screenshots/geoschelling2.JPG)


## How to run the App?

* Install Python3 ( I would recommend you to download it from [Anaconda](https://www.anaconda.com/products/individual))
* Clone the [source repository](https://github.com/kartikeyas00/geo-schelling) from Github.
* On the command line, enter:
    ````
    git clone https://github.com/kartikeyas00/geo-schelling.git
    ````
* Install the relevant libraries by doing the following:
  * Using [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) (recommended)
    * Open the terminal or an Anaconda Prompt and create a new environment
      ````
      conda env create -f environment.yml # environment.yml file is included in the project directory
      ````
    
  * Using [pip](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
    * Installing virtualenv
      ````
      python3 -m pip install --user virtualenv # On macOS and Linux
      py -m pip install --user virtualenv :: On Windows
      ````
    * Creating a virtual environment

      To create a virtual environment, go to your project’s directory and run venv.
      ````
      python3 -m venv env # On macOS and Linux
      py -m venv env :: On Windows
      ````
    * Activating a virtual environment
      ````
      source env/bin/activate # On macOS and Linux
      .\env\Scripts\activate :: On Windows
      ````
    * Install the requirements.txt file
      ````
      python3 -m pip install -r requirements.txt # On macOS and Linux
      py -m pip install -r requirements.txt :: On Windows
      ````
    
* Now go to app folder and run the run.py file
    ````
    cd geo-schelling/app
    python run.py
    ````

## About the App
The app is built with PyQt5 and PyQtGraph. It has the support for all 50 American states and more geographies can be added (Please contribute). Below are the various options available in the app.

| Option | Description |
| -----------| ------------|
| Select State | Select the state you want to run your simulation on. |
|Populate| Randomly populates the space (Selected state in this case). |
|Run| Run the simulation. Currently it runs for max 500 iterations but can be customized for more. |
|End| End the simulation. |
|Spacing| Select the space between the agents on the geographical space. |
|Empty Ratio|What percent of houses would be empty. |
|Similarity Threshold| Sets the similarity threshold (Explained above). |
|Demographic Ratio|What is the ratio between the minority and majority or between the two races. To make things more realistic you can have the real ratio for a particular state between White(Majority) and the other races(Minority)|

#### Scope for improvement
There are lot of things which can be improved and added. Some are listed below -
1. Speed can be improved as sometimes with large number of agents the model runs very slow. Currently I am using KDTree to query the Geospace which also considered to most efficient datastructure present.
2. Legends can be added to the plot as I am unable to figure out a way to add the legends, if someone can help me out with that that would be awesome.
3. Features for Data Collection can be added. For example we can collect the data for the ratio between the two races in every county of a state, after the simulation is complete.
4. Other agent based models can be implemented here.


## What is Schelling's Model of Segregation?
The Schelling model of segregation is an agent-based model that illustrates how individual tendencies regarding neighbors can lead to segregation and useful for the study of residential segregation of ethnic groups where agents represent householders who relocate in the city.

***Assumptions, Model Formation and Simulation***

#### Basic Assumption for Model
1. An agent, located in the center of a neighborhood where the fraction of friends f is less than a predefined similarity threshold F (i.e., f < F), will try to relocate to a neighborhood for which the fraction of friends is at least f.

#### Model Formation
1. Agents occupy cells of space (It can be of any shape but in this case it is of the shape of a chosen American state). A cell can be occupied by a single agent only.
2. Agents belong to one of the two races and are able to relocate according to the fraction of friends (i.e., agents of their own race) within a neighborhood around their location.

#### Basic Assumptions for Simulation
1. There can be n (2 in our case) number of races living in a space (American State).
2. Each race is represented by an unique color (in our case, white for majority and yellow for minority). Each cell in the space represents the house.
3. A house can be either empty or full. A full house can have only one person at maximum living in it. 
4. Neighbours of a person are the people living in the adjacent houses. (Up, Bottom, Left, Right, Up-Left, Up-Right, Bottom-Left, Bottom-Right)

#### Simulation
1. Randomly populate the space and leave some houses empty (given by empty ratio).
2. Every person in the space is checked if satisfied or not. If satisfied, don't do anything. If not, person is moved to an empty house.
3. Simulation is run until there is no person to be moved or for a set number of iterations.

#### Doubts?
1. Person and agent are used interchangeably.
2. A agent/person is satisfied when the ratio of neighbors of the same race is above a certain threshold (Similarity threshold), we say that the person is satisfied. If the former statement is not true then the person/agent is not satisfied.

## Motivation to build the Geographical version
The main motivation was that in lots of agent based modeling cases and especially in schelling's model of segregation, geological or geographical version is not present or when they are present they are not very well implemented. I wanted to see the schelling's model simulating on a real geography and the outcomes of the simulation as the model is based for real world. After implementing the model and visually seeing the result, I was able to conclude that how segregation can happen in the real world (Obviously if we leave certain factors alone) based on the Schelling's approach. 

## Questions ??
Don't hesitate to contact me at kartikeya2015@gmail.com
