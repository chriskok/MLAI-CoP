import sys
import os

import random
import itertools as its
import numpy as np

#import gym
#from gym.envs.toy_text import discrete
#from gym import utils

from mutils import Utils as mut


class Grid(object):

    def __init__(self, side=6):
        self.side = side
        self.agents = {}

        self.grid = np.zeros((self.side, self.side), dtype=np.int8)
        for i in range(random.randint(1, self.side*2)):
            self.grid[random.randint(0, self.side-1), random.randint(0, self.side-1)] = -1

    def locations(self):
        try:
            return self._locations
        except:
            self._locations = sorted([(ri, ci) for ci in range(self.side) for ri in range(self.side)])
            return self.locations()

    def render(self, mode='human'):
        y = ''
        import time
        mut.clear()
        for i in range(self.side):
            for j in range(self.side):
                x = ''
                for aname, agent in self.agents.items():
                    if agent.state == (i, j):
                        x += str(aname)
                x = (x + ('_'*len(self.agents)))[:len(self.agents)]
                y += x + ' '
            y += '\n'
        y += '\nPositions '
        for aname, agent in self.agents.items():
            y += aname + '(' + ', '.join([str(v) for v in agent.state]) + ') '
        y += '\n'
        print(y)
        time.sleep(.5)

    def add_agent(self, agent):
        self.agents[agent.name] = agent

    def step(self):
        moved = 0
        for name, agent in self.agents.items():
            moved += agent.move()
            self.render()
        return moved


