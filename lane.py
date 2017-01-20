import os
import sys
import math
import numpy as np
from Queue import Queue

class lane(object):

    def __init__(self, args):
        self.args = args
        self.cars  = []
        # Here kind is the type of the lane
        #0 -> normal toll with people
        #1 -> normal without people 
        #2 -> normal ETS
        self.kind = args['kind']
        self.merge_position = [5, 5, 5]
        # Whether these lane is blocked in the far place
        self.is_block = args['is_block']

    def push(self, car):
        self.cars.append(car)

    def pop(self):
        self.cars.pop(0)

    def _pre_car(self, pos):
        for car in reversed(self.cars):
            if car.position > pos:
                return car

    def _same_car(self, oth_lane, position):
        for item in oth_lane.cars:
            if item.position == position:
                return True
        return False

    def move(self):
        ret = 0
        for car in self.cars:
            car.position += 1.0
            print car.position
            if (not self.is_block) and car.position >= self.merge_position[self.kind]:
                ret = 1
                self.cars.remove(car)

        return ret

    def change_lane(self, oth_lane):
        if not self.is_block:
            return 0
        ret = 0
        for car in self.cars:
            if not self._same_car(oth_lane, car.position):
                if car.position >= self.merge_position[self.kind]:
                    ret = 1
                    self.cars.remove(car)
                else:
                    oth_lane.push(car)
                    self.cars.remove(car)
        return ret
        
                


