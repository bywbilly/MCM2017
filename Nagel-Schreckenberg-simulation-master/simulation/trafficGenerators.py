import random
import numpy as np

class SimpleTrafficGenerator():
    def __init__(self, carPerUpdate=10):
        self.queue = 0
        self.totalCars = 0
        self.carPerUpdate = carPerUpdate

    def prepare(self, road):
        pass

    def generate(self, road):
        #amount = random.randint(0, self.carPerUpdate)
        #The total number of each toll's car is a poisson distribution
        amount = 10000 * np.random.poisson(self.carPerUpdate)
        #amount = 100
        for i, item in enumerate(road.is_etc):
            if item:
                amount[i] *= road.ect_ratio
        self.totalCars = np.sum(amount)

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
        self.totalCars = 0
        self.spawnCars = 0
        self.Lambda = Lambda

    def prepare(self, road):
        #self.amount = 5 * np.random.poisson(self.Lambda, road.getLanesCount())
        #print (self.amount)
        self.amount = [1000000 for _ in range(road.getLanesCount())]
        self.totalCars = np.sum(self.amount)
        self.gap = np.random.exponential(self.Lambda, road.getLanesCount())
        self.serve_time = np.random.normal(5.5, 1.83, road.getLanesCount())
        for i, item in enumerate(road.is_etc):
            if item:
                self.gap[i] = np.random.exponential(self.Lambda * 0.75)
                self.serve_time[i] = 1.0
        self.pre_step = [0 for _ in range(road.getLanesCount())]
        for i in range(len(self.amount)):
            if self.amount[i]:
                self.pre_step[i] += max(self.gap[i], self.serve_time[i])
                print (self.pre_step[i])
        #self.pre_step = [0 for _ in range(road.getLanesCount())]

    def generate(self, road): 
        self.gap = np.random.exponential(self.Lambda, road.getLanesCount())
        self.serve_time = np.random.normal(5.5, 1.83, road.getLanesCount())
        for i, item in enumerate(road.is_etc):
            if item:
                self.gap[i] = np.random.exponential(self.Lambda * 0.75)
                self.serve_time[i] = 1.0
        added = road.pushCarsPoisson(self.amount, self.gap, self.step, self.pre_step, self.serve_time)
        self.spawnCars += np.sum(added)

        self.step += 1
        for i in range(len(self.amount)):
            if self.amount[i]:
                self.amount[i] -= added[i]
                self.pre_step[i] += added[i] * max(self.gap[i], self.serve_time[i])
