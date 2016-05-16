"""
simulation.py

`simulation.py` should specify (via a Simulation object) how to run a model
simulation. This file is a part of an example for optimizing the resurgent Na+
channel.

Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""

from neuron import h
import numpy as np
import os
import yaml

import logging
log = logging.getLogger(__name__)

class Simulation(object):
    def __init__(self, sim_vars, dt=0.1):

        h.load_file('stdrun.hoc')
        self.dt = dt
        self.sim_time = 300 # this will be rewritten in set_SEClamp
        h.celsius = 22

        #load known/default parameters
        params = yaml.load(open('params_example_start.yaml'))

        soma = h.Section(name='soma')
        soma.L = 15
        soma.diam = 15
        soma.cm = 1

        soma.insert('Narsg')
        #set known/default parameters
        for p in params['Channel']:
            cmd = 'soma(0.5).%s_Narsg = %s' % (p, params['Channel'][p])
            exec(cmd)
        #assign passed variables
        for sv in sim_vars:
            cmd = 'soma(0.5).%s_Narsg = %s' % (sv, sim_vars[sv])
            exec(cmd)
        self.recording_section = soma
        self.soma = soma

    def set_SEClamp(self, vstep):
        self.vc = h.SEClamp(0.5, sec=self.soma)
        self.vc.rs = 1 #
        self.vc.dur1 = 100
        self.vc.dur2 = 100
        self.vc.dur3 = 100
        self.vc.amp1 = -70
        self.vc.amp2 = vstep
        self.vc.amp3 = -70
        self.sim_time = self.vc.dur1 + self.vc.dur2 + self.vc.dur3

    def set_recording(self):
        #self.rec_t = h.Vector()
        #self.rec_t.record(h._ref_t)
        self.rec_ina = h.Vector()
        self.rec_ina.record(self.recording_section(0.5)._ref_ina, self.dt)

    def go(self):
        self.set_recording()
        h.dt = self.dt
        h.tstop = self.sim_time
        h.finitialize(-60)#self.v_init)
        h.init()
        h.run()

        self.rec_i = self.rec_ina.to_python()
