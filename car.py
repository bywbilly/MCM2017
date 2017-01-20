import os
import sys
import math
import numpy as np

class car(object):
    
    def __init__(self, args):
        self.args = args
        self.velocity = args['v']
        self.a = args['a']
        self.position = 0.0
        self.lane = args['lane']

