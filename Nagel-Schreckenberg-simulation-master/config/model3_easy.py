from simulation.speedLimits import *
from simulation.trafficGenerators import * 

maxFps= 40
size = width, heigth = 1280, 720
# in miliseconds
updateFrame = 500

seed = None

lanes = 7
length = 50 
etc_ratio = 0.5


#mergePos = [length - 5, length, length, length - 5, length, length, length - 5]
#length = 50

maxSpeed = 5

mergePos = [6, length, length, 6, length, length, 6]
is_main = [0, 1, 1, 0, 1, 1, 0]
is_etc  = [0, 1, 0, 0, 1, 0, 0]

speedLimits = [ 
SpeedLimit(range=((mergePos[0],0),(length,0)), limit=0, ticks=0), 
SpeedLimit(range=((mergePos[1], 1), (length,1)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[2], 2), (length,2)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[3], 3), (length,3)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[4], 4), (length,4)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[5], 5), (length,5)), limit=0, ticks=0),
SpeedLimit(range=((mergePos[6], 6), (length,6)), limit=0, ticks=0),
]

trafficGenerator = TrafficGenerator(20)

slowDownProbability, laneChangeProbability = 0.0, -1.0