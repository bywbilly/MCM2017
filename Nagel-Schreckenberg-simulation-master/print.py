import os
import sys
import matplotlib.pyplot as plt

x = [i for i in xrange(8, 19)]

y = [1027, 1029, 996, 1047, 965, 1032, 1065, 944, 1129, 981, 963]
plt.xlabel('l')
plt.ylabel('Simulation steps')
plt.axis([8, 19, 400, 1500])
plt.plot(x, y)

plt.savefig('model1_length_step_1.png')

