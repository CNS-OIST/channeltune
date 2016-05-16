"""
generate_target_navrsg.py

This file generates the sample simpulated data based on the model of
resurgent Na+ channel from Akemann and Knoepfel, J.Neurosci. 26 (2006) 4602 and
simple voltage command protocol.

Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""

from channeltune import utils
from neuron import h

w = utils.Workspace('target')

h.load_file('stdrun.hoc')

# Define a cell.
soma = h.Section(name='soma')
soma.insert('Narsg')
soma.L = 15
soma.diam = 15
soma.cm = 1

# Load original parameters
import yaml
params = yaml.load(open('params_example_original.yaml'))

for p in params['Channel']:
    exec('soma(0.5).%s_Narsg = %s' % (p, params['Channel'][p]))


h.celsius = 22.
vc = h.SEClamp(0.5, sec=soma)
vc.rs = params['SEClamp']['rs']

# Define simple voltage command protocol to interrogate the channel
# Holding period = 100ms
vc.dur1 = 100
vc.dur2 = 100
vc.dur3 = 100

# Holding potential = -70 mV, test potential, -70 mV
vc.amp1 = -70
vc.amp2 = -50
vc.amp3 = -70


h.tstop = vc.dur1+vc.dur2+vc.dur3

Dt = 0.1 # Sampling period

# Run simulations and save the data
for i, vstep in enumerate(range(-90, 40, 10)):
    vv = h.Vector()
    inav = h.Vector()
    vv.record(soma(0.5)._ref_v, Dt)
    inav.record(soma(0.5)._ref_ina, Dt)

    vc.amp2 = vstep

    h.init()
    h.run()

    data = {'amp': vstep, 'v': vv.to_python(), 'i': inav.to_python()}
    w.write_target(i, data)

h.quit()
