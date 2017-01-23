from simulation.speedLimits import *
from simulation.trafficGenerators import * 

maxFps= 40
size = width, heigth = 1280, 720
# in miliseconds
updateFrame = 500

seed = None

lanes = 13
length = 100
etc_ratio = 0.5


length = 50

maxSpeed = 5

length1 = 18
mergePos = [3, length1, length, 5, 3, length1, length, length1, 3, 5, length, length1, 3]
is_main = [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
is_etc  = [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0]

speedLimits = [ 
SpeedLimit(range=((mergePos[0],0),(length,0)), limit=0, ticks=0), 
SpeedLimit(range=((mergePos[1], 1), (length,1)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[2], 2), (length,2)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[3], 3), (length,3)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[4], 4), (length,4)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[5], 5), (length,5)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[6], 6), (length,6)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[7], 7), (length,7)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[8], 8), (length,8)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[9], 9), (length,9)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[10], 10), (length,10)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[11], 11), (length,11)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[12], 12), (length,12)), limit=0, ticks=0),
]
trafficGenerator = TrafficGenerator(30)

slowDownProbability, laneChangeProbability = 0.0, -1.0
