import os
import sys
sys.path.append(os.path.abspath('..'))

import Experiments.ExperimentObjects as exp


def run():
    exp.main("Investigation of Newton's 2nd Law")

if __name__ == '__main__':
    run()
