import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as exp


def run():
    exp.main("Internal Resistance of a Battery")

if __name__ == '__main__':
    run()
