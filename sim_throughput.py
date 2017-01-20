import os
import sys
import math
import numpy as np
import argparse

from gen_car import gen_car
from car import car
from lane import lane

def trivial_sim(args, L, B):

    Gen_car = gen_car(args_gen_car)
    Gen_car.prepare()
    
    lanes = []

    delta = B - L
    for i in xrange(B):
        lane_args = {}
        lane_args ['is_block'] = 1 if i < delta or B - i < delta else 0
        lane_args['kind'] = 0
        lanes.append(lane(lane_args))

    throughput = 0
    T = 0.0
    T_upper = 100.0

    while T < T_upper:
        # Move each car
        for i in xrange(B):
            merge = lanes[i].move()
            throughput += merge
        # Try to change lane
        for i in xrange(B):
            merge = lanes[i].change_lane(lanes[i + 1 if i < 2 else i - 1])
            throughput += merge

        cars = Gen_car.nxt_event(T)
        for item in cars:
            _, index = item
            car_args = {}
            car_args['v'] = 0
            car_args['a'] = 0
            car_args['lane'] = index
            print 'index:'
            print index
            lanes[index].push(car(car_args)) 

        T += 0.1
    
    print 'The throughput is: %d\n' % throughput

   

if __name__ == '__main__':

    argparser = argparse.ArgumentParser(sys.argv[0])
    argparser.add_argument('--Lambda', type=float, default=1)
    argparser.add_argument('--B', type=int, default=8)
    argparser.add_argument('--L', type=int, default=4)

    args = argparser.parse_args()

    args_gen_car = {'lambda': args.Lambda, 'lane': args.B}

    trivial_sim(args_gen_car, args.L, args.B)





