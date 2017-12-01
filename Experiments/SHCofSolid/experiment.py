import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as exp


def run():
    exp.main("Specific Heat Capacity of a Solid")

if __name__ == '__main__':
    run()
