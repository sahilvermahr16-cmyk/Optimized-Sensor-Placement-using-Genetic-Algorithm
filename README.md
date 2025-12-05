# Optimized-Sensor-Placement-using-Genetic-Algorithm
A Genetic Algorithm approach to maximize building coverage using air-quality sensors.

# Overview

This project implements an optimization system that determines the best placement of air-quality sensors inside a 2D building grid. Because each sensor covers only a limited circular area, choosing sensor positions manually is difficult and inefficient.

A Genetic Algorithm (GA) is used to automatically search for high-quality sensor arrangements that:

Maximize coverage

Minimize cost

This assignment demonstrates how evolutionary algorithms can be used to solve real-world optimization problems.

# Problem Statement

Given: A 2D grid of size:

                  WIDTH×HEIGHT

N sensors to place, Each sensor has a coverage radius R, Deployment cost defined per sensor (NUM_SENSORS)

Determine the positions of the sensors that maximize the fitness function:

      Fitness=CoverageScore−α*SensorCost

Where: 

- CoverageScore = number of cells covered one sensor

- SensorCost = number of sensors

- α = cost weight (0 = ignore cost)
