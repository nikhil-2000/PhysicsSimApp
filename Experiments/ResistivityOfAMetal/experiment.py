import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as exp


def run():
    exp.main("Determination Of the Resistivity Of A Metal")

if __name__ == '__main__':
    run()
