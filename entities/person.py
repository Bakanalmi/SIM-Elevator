from numpy import random
import math


class Persona:
    def __init__(self, env, values, ident):
        self.env = env
        self.latest = 0
        self.id = ident

        upper = values.get('environment').get('n_floors')
        floor = random.uniform(upper, 1, size=1)

        choose_stairs = random.exponential() % 1
        self.walker = values.get('environment').get('stairs') and choose_stairs > values.get('stairs').get('range')

        self.currentFloor = 0
        self.dest = floor
