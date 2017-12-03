import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as exp


def run():
    exp.main("Estimating Absolute Zero Using Gas Laws")

if __name__ == '__main__':
    run()
