from simulation.speedLimits import *
from simulation.trafficGenerators import * 

maxFps= 40
size = width, heigth = 1280, 720
# in miliseconds
updateFrame = 500

seed = None

lanes = 2
length = 100
etc_ratio = 0.5


#mergePos = [length - 40, length, length - 40, length, length - 40, length, length - 40]
length = 10
length1 = 9

maxSpeed = 5

#mergePos = [5, 10, 15, 20, 30, length, length, length, 30, 20, 15, 10, 5]
#is_main = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0]
#is_etc  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mergePos = [length1, length]
is_main = [0, 1]
is_etc = [0, 0]

speedLimits = [ 
SpeedLimit(range=((mergePos[0],0),(length,0)), limit=0, ticks=0), 
SpeedLimit(range=((mergePos[1], 1), (length,1)), limit=0, ticks=0),
]
trafficGenerator = TrafficGenerator(2)

slowDownProbability, laneChangeProbability = 0.0, -1.0
