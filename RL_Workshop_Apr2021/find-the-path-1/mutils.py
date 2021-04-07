import sys
import os
import random


class Utils(object):

    @staticmethod
    def clear():
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')
        else:
            sys.exit(-1)
        print()


    @staticmethod
    def random_distribute(le):
        shares = []
        full = 1
        a = {}
        for i in range(le):
            if i == 0:
                continue
            share = full * random.random()
            shares.append(share)
            full -= share
        shares.append(full)
        assert sum(shares) == 1
        return shares


class Graph(object):

    def __init__(self):
        self.root = None
        self.last_id = 0


class Node(object):

    def __init__(self, reward=0):
        self.id = id
        self.neighbors = {}
        self.reward = 0