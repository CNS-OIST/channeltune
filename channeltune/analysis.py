"""
analysis.py

This module computes fitness given the target and simulation results.


Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""


import scipy.stats
import numpy as np
import math
from inspyred.ec import emo

class VClampAnalysis(object,):
    def __init__(self, currents):
        self.currents = currents

    def analyse(self,
                targets,
                target_weights,
                cost_function):
        """ Helper function for evaluate_fitness. It is currently blank as the recordings are compared to each other _directly_ without comparing statistical parameters"""

        analysis_results={}

    def evaluate_fitness(self, targets):
        results = []
        for i, _ in enumerate(self.currents):
            # evaluate the difference for each current
            diff = 0.
            for j, _ in enumerate(targets[i]):
                # evaluate error squared sum
                diff = diff + (targets[i][j]-self.currents[i][j])**2
            results.append(diff)
        return emo.Pareto(results)
