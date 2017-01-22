import random
import numpy as np

class SimpleTrafficGenerator():
    def __init__(self, carPerUpdate=10):
        self.queue = 0
        self.carPerUpdate = carPerUpdate

    def prepare(self, road):
        pass

    def generate(self, road):
        #amount = random.randint(0, self.carPerUpdate)
        #The total number of each toll's car is a poisson distribution
        #amount = np.random.poisson(self.carPerUpdate)
        amount = 100
        self.tryGenerate(road, amount)

    def tryGenerate(self, road, amount):
        added = road.pushCarsRandomly(amount + self.queue)
        self.queue += (amount - added)

class TrafficGenerator():

    def __init__(self, Lambda=1):
        self.gap = []
        self.amount = []
        self.pre_step = []
        self.serve_time = []
        self.step = 0
        self.Lambda = Lambda

    def prepare(self, road):
        #self.amount = np.random.poisson(self.Lambda, road.getLanesCount())
        self.amount = [10 for _ in range(road.getLanesCount())]
        self.gap = np.random.exponential(self.Lambda, road.getLanesCount())
        self.serve_time = np.random.normal(5.5, 1.83, road.getLanesCount())
        self.pre_step = [0 for _ in range(road.getLanesCount())]
        for i in range(len(self.amount)):
            if self.amount[i]:
                self.pre_step[i] += max(self.gap[i], self.serve_time[i])
                print (self.pre_step[i])
        #self.pre_step = [0 for _ in range(road.getLanesCount())]

    def generate(self, road): 
        self.gap = np.random.exponential(self.Lambda, road.getLanesCount())
        self.serve_time = np.random.normal(5.5, 1.83, road.getLanesCount())
        added = road.pushCarsPoisson(self.amount, self.gap, self.step, self.pre_step, self.serve_time)

        self.step += 1
        for i in range(len(self.amount)):
            if self.amount[i]:
                self.amount[i] -= added[i]
                self.pre_step[i] += added[i] * max(self.gap[i], self.serve_time[i])
