"""
optimizer.py

This module specifies details about the optimization algorithm.


Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""


import evaluator
import os
from inspyred import ec
from inspyred.ec import observers
from inspyred.ec import terminators
from inspyred.ec import selectors
from inspyred.ec import replacers
from inspyred.ec import variators
from random import Random
from time import time

class Optimizer(object):
    def __init__(self, max_constraints, min_constraints,evaluator,
                 mutation_rate=0.2, max_evaluations=100,
                 maximize=False,
                 seeds=[], population_size=10,
                 num_selected=None,
                 tourn_size=2,
                 num_elites=1,
                 num_offspring=None):
        self.max_constraints=max_constraints
        self.min_constraints=min_constraints
        self.evaluator=evaluator
        self.population_size=population_size
        self.maximize=maximize
        self.max_evaluations=max_evaluations
        self.tourn_size=tourn_size
        self.num_elites=num_elites
        self.mutation_rate=mutation_rate
        self.seeds=seeds
        if num_selected==None:
            self.num_selected=population_size
        else:
            self.num_selected=num_selected
        if num_offspring==None:
            self.num_offspring=population_size-self.num_selected
        else:
            self.num_offspring=num_offspring

    def uniform_random_x(self,random,args):
        varxs = []
        for lo, hi in zip(self.max_constraints, self.min_constraints):
            varxs.append(random.uniform(lo, hi))
        return varxs

    def optimize(self,do_plot=True):
        rand = Random()
        rand.seed(int(time()))

        cwd=os.getcwd()
        datadir=os.path.dirname(cwd)+'/data/'
        if not os.path.exists(datadir):
            os.mkdir(datadir)

        stat_file_name=datadir+'/ga_statistics.csv'
        ind_file_name=datadir+'/ga_individuals.csv'
        stat_file = open(stat_file_name, 'w')
        ind_file = open(ind_file_name, 'w')

        algorithm = ec.emo.NSGA2(rand) #ec.EvolutionaryComputation(rand)
        algorithm.observer = observers.file_observer
        algorithm.terminator = terminators.evaluation_termination
        algorithm.selector = selectors.tournament_selection
        algorithm.replacer = replacers.steady_state_replacement
        algorithm.variator = [variators.blend_crossover, variators.gaussian_mutation]

        final_pop = algorithm.evolve(generator=self.uniform_random_x,
                 evaluator=self.evaluator.evaluate,
                 pop_size=self.population_size,
                 maximize=False,
                 bounder=ec.Bounder(lower_bound=self.min_constraints,
                                    upper_bound=self.max_constraints),
                 num_selected=self.num_selected,
                 tourn_size=self.tourn_size,
                 num_elites=self.num_elites,
                 num_offspring=self.num_offspring,
                 max_evaluations=self.max_evaluations,
                 mutation_rate=self.mutation_rate,
                 statistics_file=stat_file,
                 seeds=self.seeds,
                 individuals_file=ind_file)
        stat_file.close()
        ind_file.close()
        self.print_report(final_pop,do_plot,stat_file_name)

    def print_report(self,final_pop,do_plot,stat_file_name):
        print(max(final_pop))
        #Sort and print the fitest individual, which will be at index 0.
        final_pop.sort(reverse=True)
        print ('\nfitest individual:')
        print(final_pop[0])
