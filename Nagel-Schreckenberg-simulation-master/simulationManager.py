import pygame
import matplotlib.pyplot as plt
import numpy as np

class SimulationManager:
    def __init__(self, road, trafficGenerator, updateFrame):
        self.road = road
        self.trafficGenerator = trafficGenerator
        self.updateFrame = updateFrame
        self.acc = 0
        self.cnt = 0
        self.timeFactor = 0.0
        self.prevTimeFactor = 1.0
        self.running = True
        self.stepsMade = 0

    def update(self, dt):
        self.acc += dt * self.timeFactor
        limit = 0
        if self.acc >= self.updateFrame:
            self.acc = self.acc % (self.updateFrame + 0)
            self.makeStep()

    def makeSteps(self, steps):
        for x in range(steps): self.makeStep()

    def print_step_accidentRate(self):
        #print (self.road.print_accidentRate)
        plt.plot(self.road.print_accidentRate)
        plt.ylabel('AccidentRate')
        plt.xlabel('SimulationStep')
        #plt.show()
        plt.savefig('Step_AccidentRate.png')


    def makeStep(self):
        if not self.stepsMade:
            self.trafficGenerator.prepare(self.road)
        self.trafficGenerator.generate(self.road)
        self.road.update();
        self.stepsMade += 1
        #print (self.trafficGenerator.totalCars, self.road.deadCars, self.trafficGenerator.spawnCars)
        #if self.trafficGenerator.totalCars <= self.road.deadCars:
        if self.road.deadCars >= 30 or  self.road.getAvgCarSpeed()[1] == 0:
            self.cnt += 1
            if self.road.deadCars >= 30 or self.cnt == 20:
            #self.print_step_accidentRate()
                print ('Simulation steps:')
                print (self.road.updates)
                print ('Accident ratio')
                print (self.road.deltaV)
                accident_ratio = 5 + 0.8 * np.power(self.road.deltaV, 2) + 0.014 * np.power(self.road.deltaV, 3)
                print (accident_ratio)
                print ('Average Speed:')
                print (self.road.avgSpeed / float(self.road.updates - 20.0))
                print ('Passed Cars:')
                print (self.road.deadCars)
                self.running = False
        else:
            self.cnt = 0

    def processKey(self, key):
        {
            pygame.K_ESCAPE: self.__exit,
            pygame.K_SPACE:  self.__pauseSwitch,
            pygame.K_m: self.__speedUp,
            pygame.K_n: self.__speedDown,
            pygame.K_s: self.__oneStepForward,
            pygame.K_d: self.__manyStepsForward(500)
        }.get(key, lambda: print("Unknown key"))()

    def isStopped(self):
        return self.timeFactor == 0

    def __exit(self): 
        self.running = False
        print ('Simulation steps:')
        print (self.road.updates)
        print ('Accident ratio')
        print (self.road.deltaV)
        accident_ratio = 500 + 0.8 * np.power(self.road.deltaV, 2) + 0.014 * np.power(self.road.deltaV, 3)
        print (accident_ratio)
        print ('Average Speed:')
        print (self.road.avgSpeed / float(self.road.updates - 20.0))
        print ('Passed Cars:')
        print (self.road.deadCars)

    def __pauseSwitch(self):
        self.timeFactor, self.prevTimeFactor = self.prevTimeFactor, self.timeFactor
    def __speedUp(self): self.timeFactor = min(8.0, self.timeFactor*2)
    def __speedDown(self): self.timeFactor = max(1/8, self.timeFactor/2)
    def __oneStepForward(self):
        if self.isStopped(): self.makeStep()
        else: print("Can't make step: simulation is running")
    def __manyStepsForward(self, steps):
        def manySteps():
            self.makeSteps(steps)
        return manySteps

