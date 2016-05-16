"""
utils.py

Utility functions and objects for data I/O, etc.


Written by Sergei Zobnin and Sungho Hong, CNS unit, OIST
December 2015

"""


import os
import pickle

def mkdirp(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


class Workspace(object):
    def __init__(self, path='target', current_name='i', control_param_name='amp'):
        super(Workspace, self).__init__()

        self.root = os.path.abspath(os.getcwd())
        self.target = mkdirp(os.path.join(os.path.abspath(self.root), path))
        self.current_name = current_name
        self.control_param_name = control_param_name

    @classmethod
    def from_path(cls, path):
        wplace = os.path.dirname(path)
        return cls(wplace)

    def in_root(self, x):
        return os.path.join(self.root, x)

    def in_target(self, x):
        return os.path.join(self.target, x)

    def write_target(self, i, data):
        with open(self.in_target('data_%d.pkl' % i), 'w') as f:
            pickle.dump(data, f)

    def list_objectives(self):
        x = [f for f in os.listdir(self.target) if f.startswith('data')]
        x = [int(f.strip('.pkl').strip('data_')) for f in x]
        x.sort()
        return x

    def load_objective(self, i):
        fname = self.in_target('data_%d.pkl' % i)
        if not os.path.exists(fname):
            raise RuntimeError(fname + 'does not exist')
        with open(fname) as f:
            datadic = pickle.load(f)
        return (datadic[self.control_param_name], datadic[self.current_name])
