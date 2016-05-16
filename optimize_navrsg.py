"""
optimize_navrsg.py

An example of optimizing the resurgent Na+ channel model using channeltune.

Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""


from channeltune import optimizer, evaluator, controller, utils

def main():
    wspace = utils.Workspace()
    sxController = controller.Controller('simulation', wspace, parallelcontext='ipyparallel')

    parameters = ['gbar', 'x1', 'x2'] #parameters to be modified in each simulation
    min_constraints = [0., 10., -45.] #their boundaries
    max_constraints = [0.1, 70., -10.]

    vsteps = range(-90, 40, 10)

    sxEvaluator=evaluator.Evaluator(controller=sxController,
                                    parameters=parameters,
                                    objectives=wspace.list_objectives())

    sxOptimizer=optimizer.Optimizer(max_constraints,
                                    min_constraints,
                                    sxEvaluator,
                                    population_size=5000,
                                    max_evaluations=25000,
                                    num_selected=100,
                                    num_offspring=25,
                                    num_elites=50,
                                    seeds=None)

    sxOptimizer.optimize()


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='example1.log', level=logging.DEBUG)
    main()
