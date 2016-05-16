"""
controller.py

This module specifies how to make a master controller object, Controller.


Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""


import os
import importlib
import numpy as np
import logging

log = logging.getLogger(__name__)

class Controller(object):
    def __init__(self, simulation_module_name,
                       workspace,
                       parallelcontext='multiprocessing'):

        self.simulation_module_name = simulation_module_name
        self.workspace = workspace
        self.parallelcontext = parallelcontext

    def run(self, candidate_params):
        candidates = candidate_params[0]
        parameters = candidate_params[1]
        self.vsteps = vsteps
        traces = []
        #log.debug('Candidates are ' + str(candidates))
        #log.debug('Parameters are ' + str(parameters))
        for candidate in candidates:
            sim_var = dict(zip(parameters, candidate))
            traces.append(self.run_individual(sim_var))
        return traces

    def run_individual(self, candidate_params):
        simulation = importlib.import_module(self.simulation_module_name)

        candidates = candidate_params[0]
        parameters = candidate_params[1]
        self.vsteps = candidate_params[2]

        sim_var = dict(zip(parameters,candidates))
        sim = simulation.Simulation(sim_var)

        t_results = [] #multiple recordings of a variable

        for vstep in self.vsteps:
            sim.set_SEClamp(vstep)
            sim.go()
            t_results.append(sim.rec_i)
        return t_results
