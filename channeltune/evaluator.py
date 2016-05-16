"""
evaluator.py

This module specifies Evaluator objects that handles evaluating fitness of candidates.


Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""

import os, sys
import controller
import numpy
import utils

import logging

log = logging.getLogger(__name__)


class multiproc_view(object):
    def map(self, f, args):
        from multiprocessing import Pool
        from contextlib import closing

        with closing(Pool()) as p:
            fitness = p.map(f, args)
        return fitness


def evaluateCandidate(args):
    import analysis

    sxController = args[0]
    pars = args[1:]
    targets = pars[-1]
    sim_data = sxController.run_individual(pars[:-1])
    an = analysis.VClampAnalysis(sim_data)
    return an.evaluate_fitness(targets)


class Evaluator(object):
    def __init__(self,
                 controller,
                 parameters,
                 objectives):
        self.controller = controller
        self.parameters = parameters
        self.objectives = objectives

        #get recordings from files
        self.control_params = []
        self.targets = []
        for i in self.objectives:
            c1, t1 = self.controller.workspace.load_objective(i)
            self.control_params.append(c1)
            self.targets.append(t1)

        self.generation = 0

        if self.controller.parallelcontext == 'multiprocessing':
            self.multiview = multiproc_view()
        elif self.controller.parallelcontext == 'ipyparallel':
            from ipyparallel import Client
            lview = Client().load_balanced_view()
            lview.block = True
            self.multiview = lview
        else:
            raise RuntimeError('Unknown parallelcontext')

    def evaluate(self, candidates, args):

        self.generation = self.generation + 1

        evaluator_args = []

        for cand in candidates:
            evaluator_args.append([self.controller, cand, self.parameters, self.control_params, self.targets])

        fitness = self.multiview.map(evaluateCandidate, evaluator_args)

        # Cheap and dirty logging
        log.debug('Generation = %d ' % self.generation)
        for i, _ in enumerate(fitness):
            log.debug('Cadidate = %d' % i)
            log.debug(str(candidates[i]))
            log.debug('Total error = %g' % sum(fitness[i]))

        return fitness
