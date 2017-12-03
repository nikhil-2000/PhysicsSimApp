import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as exp


def run():
    exp.main("Measuring g by freefall")

if __name__ == '__main__':
    run()
