import simulation.speedLimits, random
from functools import reduce
from simulation.car import Car

class Road:
    def __init__(self, lanesCount, length, speedLimits, is_main):
        self.lanes = Road.generateEmptyLanes(lanesCount, length)
        self.updatedLanes = Road.generateEmptyLanes(lanesCount, length)
        self.speedLimits = speedLimits if speedLimits != None else simulation.speedLimits.SpeedLimits([], 5)
        # stats
        self.deadCars = 0 # cars that are gone
        self.updates = 0
        self.is_main = is_main
        print (is_main)
        self.lanesCount = lanesCount
        self.move_dir = [0 for _ in range(lanesCount)]
        self.laneChange = 0
        self.accident_rate = 0.0

    def __updateCars(self, action):
        for lane in self.lanes:
            for entity in lane:
                if entity != None:
                    newPos = action(entity)
                    if self.inBounds(newPos):
                        self.updatedLanes[int(newPos[1])][int(newPos[0])] = entity
                    else: self.deadCars += 1
        self.flipLanes()

    def updateAccidentRate(self, accident_rate):
        self.accident_rate += accident_rate
        self.laneChange += 1

    def changeDir(self, pos, move_dir):
        self.move_dir[pos[1]] = move_dir

    def update(self):
        self.laneChange = 0
        self.accident_rate = 0.0
        self.speedLimits.update()
        self.move_dir = [0 for _ in range(self.lanesCount)]
        self.__updateCars(lambda x: x.updateLane())
        self.__updateCars(lambda x: x.updateX())
        self.updates += 1
        if self.laneChange != 0:
            self.accident_rate /= float(self.laneChange)

    def flipLanes(self):
        self.lanes = self.updatedLanes
        self.updatedLanes = Road.generateEmptyLanes(self.getLanesCount(), self.getLength())

    def addCar(self):
        if self.lanes[0][0] == None:
            self.lanes[0][0] = Car(self, (0,0))
            return True
        else:
            return False

    def pushCarsPoisson(self, amount, gap, step, pre_step, serve_time):
        ret = [0 for _ in range(self.getLanesCount())]
        for i in range(self.getLanesCount()):
            if not amount[i]:
                continue
            start_step = pre_step[i] + serve_time[i] 
            if start_step < step:
                car = Car(self, (0, i), 0)
                if self.placeObject(car):
                    ret[i] = 1
        return ret

        

    def pushCars(self, amount):
        return self.__pushCars(amount, [x for x in reversed(range(self.getLanesCount()))])

    def pushCarsRandomly(self, amount):
        lanes = [x for x in range(self.getLanesCount())]
        random.shuffle(lanes)
        return self.__pushCars(amount, lanes)

    def __pushCars(self, amount, lanes):
        if not amount or not lanes: return 0
        else:
            lane = lanes.pop()
            car = Car(self, (0, lane), self.speedLimits.maxSpeed)
            if(self.placeObject(car)):
                return 1 + self.__pushCars(amount - 1, lanes)
            else:
                return self.__pushCars(amount, lanes)

    def carCount(self):
        return sum( reduce(lambda x, y: x+(0 if y == None else 1), lane, 0) for lane in self.lanes)

    def getSpeedLimitAt(self, pos):
        return self.speedLimits.getLimit(pos)

    def distanceToNextThing(self, pos):
        """Counts distance between given pos and next object (car or obstacle), takes into considerations stops (speedLimit set to 0)"""
        return self.__distanceToNextThing((pos[0]+1, pos[1]))
    def __distanceToNextThing(self, pos):
        #print (pos)
        #print (self.lanes[pos[1]])
        if pos[0] >= self.getLength():
            return self.getLength() # heaven
        else:
            #if self.lanes[pos[1]][pos[0]] == None:
            #    print("!!!")
            if self.lanes[pos[1]][pos[0]] == None and not self.speedLimits.shouldStop(pos):
                return 1 + self.__distanceToNextThing((pos[0]+1, pos[1]))
            else:
                return 0

    def getMaxSpeedAt(self, pos):
        return min(self.getSpeedLimitAt(pos), self.distanceToNextThing(pos))

    def findPrevCar(self, pos):
        if not self.inBounds(pos) or self.getSpeedLimitAt(pos) == 0: return None
        else:
            if self.lanes[pos[1]][pos[0]] != None:
                return self.lanes[pos[1]][pos[0]]
            else:
                return self.findPrevCar( (pos[0] - 1, pos[1]) )

    def findNxtCar(self, pos):
        if not self.inBounds(pos) or self.getSpeedLimitAt(pos) == 0:
            return None
        else:
            if self.lanes[pos[1]][pos[0]] != None:
                return self.lanes[pos[1]][pos[0]]
            else:
                return self.findNxtCar( (pos[0] + 1, pos[1]) )

    def possibleLaneChange(self, pos):
        if self.is_main[pos[1]]:
            return False
        else:
            return True
        
    def possibleLaneChangeUp(self, pos):
        return self.__possibleLaneChange(pos, pos[1]-1)
    def possibleLaneChangeDown(self, pos):
        return self.__possibleLaneChange(pos, pos[1]+1)
    def __possibleLaneChange(self, pos, destLane):
        if not self.inBounds( (0, destLane) ) or self.lanes[destLane][pos[0]] != None: return False
        else:
            sourceLane = pos[1]
            #print (sourceLane, destLane)
            oneMoreLane = destLane + (destLane - sourceLane)
            #print (oneMoreLane)
            if self.inBounds((0, oneMoreLane)) and self.move_dir[oneMoreLane] == sourceLane - destLane:
                return False

            if not self.inBounds( (0, oneMoreLane) ): return True
            else:
                if self.lanes[oneMoreLane][pos[0]] == None:
                    return True
                else:
                    return self.move_dir[oneMoreLane] != sourceLane - destLane
                #return self.lanes[oneMoreLane][pos[0]] == None

    def inBounds(self, pos):
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.getLength() and pos[1] < self.getLanesCount()

    def clearAt(self, pos):
        self.lanes[pos[1]][pos[0]] = None

    def placeObjects(self, entities):
        return all(self.placeObject(entity) for entity in entities)

    def placeObject(self, entity):
        if (not self.inBounds(entity.pos)
                or self.lanes[entity.pos[1]][entity.pos[0]] != None
                or self.getSpeedLimitAt(entity.pos) == 0): return False
        else:
            self.lanes[entity.pos[1]][entity.pos[0]] = entity
            return True

    def getLength(self):
        return len(self.lanes[0])
    def getLanesCount(self):
        return len(self.lanes)
    def getCellCount(self):
        return self.getLength() * self.getLanesCount()
    def getAvgCarSpeed(self):
        total = 0
        cars = 0
        for lane in self.lanes:
            for entity in lane:
                if entity != None:
                    cars += 1
                    total += entity.velocity
        return (cars, total/cars if cars > 0 else 0)

    def generateEmptyLanes(lanesCount, length):
        lanes = []
        for x in range(lanesCount):
            lanes.append( [None] * length )
        return lanes
