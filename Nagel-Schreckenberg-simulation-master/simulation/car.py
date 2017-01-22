import random
import numpy as np

class Car:
    slowDownProbability = 0
    laneChangeProbability = 0
    def __init__(self, road, pos, velocity = 0, acclerate = 1):
        self.velocity = velocity
        self.pre_velocity = 0
        self.acclerate = acclerate
        self.follow_args = {
                'm': 1,
                'l': 3,
                'a': 2.46
        }
        self.road = road
        self.pos = pos
        self.prevPos = pos
        self.priority = False

    def updateLane(self):
        self.prevPos = self.pos
        #self.priority = False
        if (not self.road.possibleLaneChange(self.pos)) and self.velocity != 0:
            return self.pos
        flip = random.random()
        go_up, accident_rate_up = self.willingToChangeUp()
        go_down, accident_rate_down = self.willingToChangeDown()
        if flip > 0.5:
            if go_up:
                if random.random() >= Car.laneChangeProbability:
                    self.pos = self.pos[0], self.pos[1]-1
                    self.road.changeDir(self.pos, -1)
                    self.road.updateAccidentRate(accident_rate_up)
            elif go_down:
                if random.random() >= Car.laneChangeProbability:
                    self.pos = self.pos[0], self.pos[1]+1
                    self.road.changeDir(self.pos, 1)
                    self.road.updateAccidentRate(accident_rate_down)
        else:
            if go_down:
                if random.random() >= Car.laneChangeProbability:
                    self.pos = self.pos[0], self.pos[1]+1
                    self.road.changeDir(self.pos, 1)
                    self.road.updateAccidentRate(accident_rate_down)
            elif go_up:
                if random.random() >= Car.laneChangeProbability:
                    self.pos = self.pos[0], self.pos[1]-1
                    self.road.changeDir(self.pos, -1)
                    self.road.updateAccidentRate(accident_rate_up)
        return self.pos

    def updateX(self):
        self.pre_velocity = self.velocity
        self.velocity = max(0, self.calcNewVelocity())
        self.acclerate = self.calcNewAcclerate()
        #print(self.acclerate)

        #if self.velocity > 0 and random.random() <= Car.slowDownProbability:
        #    self.velocity -= 1
        #print(self.pos[0], self.velocity)
        self.pos = int(self.pos[0] + self.velocity), self.pos[1]
        return self.pos

    #def calcNewVelocity(self):
    #    return min(self.velocity + 1, self.road.getMaxSpeedAt(self.pos))

    def calcNewVelocity(self):
        return min(self.velocity + self.acclerate, self.road.getMaxSpeedAt(self.pos))

    #def calcNewAcclerate(self):
    #    pre_car = self.road.findNxtCar((self.pos[0] + 1, self.pos[1]))
    #    if pre_car is None or pre_car.prevPos[0] == self.prevPos[0]:
    #        return 1
    #    m, l, a = self.follow_args['m'], self.follow_args['l'], self.follow_args['a']
    #    #print (np.abs(pre_car.prevPos[0] - self.prevPos[0]))
    #    #print(self.velocity)
    #    return a * np.power(self.velocity, m) * (pre_car.pre_velocity - self.pre_velocity) / (np.power(np.abs(pre_car.prevPos[0] - self.prevPos[0]), l))

    #simple linear following model
    def calcNewAcclerate(self):
        pre_car = self.road.findNxtCar((self.pos[0] + 1, self.pos[1]))
        if pre_car is None or pre_car.prevPos[0] == self.prevPos[0]:
            return 1
        new_acc = pre_car.pre_velocity - self.pre_velocity 
        if 3.0 < np.abs(new_acc):
            new_acc = np.sign(new_acc) * 3.0
        return new_acc
        

    def willingToChangeUp(self):
        #print("-----------------------------")
        #print(self.pos)
        ret = 0.0
        ret1, ret2 = False, False
        if self.road.possibleLaneChangeUp(self.pos):
            ret1 = True
        if self.pos[1] > 0 and self.__willingToChangeLane(self.pos[1], self.pos[1] - 1)[0]:
            ret = self.__willingToChangeLane(self.pos[1], self.pos[1] - 1)[1]
            ret2 = True
        if ret1 and ret2:
            return True, ret
        else:
            if ret1 == False and ret2 == True:
                self.priority = True
                return True, ret

        return False, ret

        #return self.road.possibleLaneChangeUp(self.pos) and self.__willingToChangeLane(self.pos[1], self.pos[1] - 1)
    def willingToChangeDown(self):
        ret = 0.0
        ret1, ret2 = False, False
        if self.road.possibleLaneChangeDown(self.pos):
            ret1 = True
        if self.pos[1] < 6 and self.__willingToChangeLane(self.pos[1], self.pos[1] + 1)[0]:
            ret = self.__willingToChangeLane(self.pos[1], self.pos[1] + 1)[1]
            ret2 = True
        if ret1 and ret2:
            return True, ret
        else:
            if ret1 == False and ret2 == True:
                self.priority = True
                return True, ret

        return False, ret
        #return self.road.possibleLaneChangeDown(self.pos) and self.__willingToChangeLane(self.pos[1], self.pos[1] + 1)

    def __willingToChangeLane(self, sourceLane, destLane):
        #print (sourceLane, destLane)
        #print ("!")
        srcLaneSpeed = self.road.getMaxSpeedAt( (self.pos[0], sourceLane) )
        destLaneSpeed = self.road.getMaxSpeedAt( (self.pos[0], destLane) )
        if destLaneSpeed == 0: return (False, 0.0)
        #if destLaneSpeed <= srcLaneSpeed: return False
        prevCar = self.road.findPrevCar( (self.pos[0], destLane) )
        if prevCar == None: return (True, 0.0)
        else:
            distanceToPrevCar = self.pos[0] - prevCar.pos[0]
            safeDistance = prevCar.velocity + 1.0 / 6.0 * np.power(prevCar.velocity, 2) + 1
            return (distanceToPrevCar > safeDistance, safeDistance / distanceToPrevCar)
            #return distanceToPrevCar > prevCar.velocity + 1.0 / 6.0 * np.power(prevCar.velocity, 2) + 1
