from numpy import random


class Person:
    def __init__(self, values, ident):
        random.seed(values.get('seed'))
        self.latest = 0
        self.id = ident

        upper = values.get('environment').get('n_floors')
        floor = random.randint(1, upper)

        choose_stairs = random.randint(0, 100)
        self.walker = values.get('environment').get('stairs') and choose_stairs < 20

        self.currentFloor = 0
        self.dest = floor
