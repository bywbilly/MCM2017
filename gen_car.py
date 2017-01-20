import os
import sys
import math
import numpy as np

from Queue import PriorityQueue

class gen_car(object):

    def __init__(self, args):
        self.args = args
        self.Lambda = args['lambda']
        self.event = PriorityQueue()
        self.lane = args['lane']

    def _gen_cnt_car(self):
        return np.random.poisson(self.Lambda)

    def _gen_gap_car(self):
        ret = list(np.random.exponential(self.Lambda, self._gen_cnt_car()))
        cnt= 0.0
        for i, item in enumerate(ret):
            cnt += item
            ret[i] = cnt
        print ret
        return ret


    def prepare(self):
        for i in xrange(self.lane):
            for car in self._gen_gap_car():
                self.event.put((car, i))

    def nxt_event(self):
        ret = []

        if not self.event.empty():
            time, lane = self.event.get()
            ret.append((time, lane))
            
        while not self.event.empty():
            time, lane = self.event.get()
            if time != ret[0][0]:
                self.event.put((time, lane))
                break
            else:
                self.event.put((time, lane))

        return ret

    def nxt_event(self, cur_time):
        ret = []

        if not self.event.empty():
            time, lane = self.event.get()
            if time < cur_time and time + 0.1 > cur_time:
                ret.append((time, lane))
            else:
                self.event.put((time, lane))

        while not self.event.empty():
            time, lane = self.event.get() 
            if time >= cur_time or time + 0.1 <= cur_time:
                self.event.put((time, lane))
                break
            else:
                ret.append((time, lane))
                self.event.get()

        return ret


        



