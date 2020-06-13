from numpy import random
from entities import token
from resources import floor
import simpy, math

class Token:
    def __init__(self, env, entry, values):
        self.counter = 0
        self.env = env
        self.entry = entry
        self.values = values
        self.MAX = values.get('environment').get('n_floors') * values.get('environment').get('cap_floor')

        random.seed(values.get('seed'))

    def new_token(self):
        while self.MAX > self.counter:
            loc = self.values.get('arrival').get('loc')
            scale = self.values.get('arrival').get('scale')
            size = self.values.get('arrival').get('size')

            upper = self.values.get('arrival').get('upper')
            lower = self.values.get('arrival').get('lower')

            howmay = math.ceil(random.normal(loc=loc, scale=scale, size=1))
            
            for iterator in range(0, howmay):
                person = token.Persona(self.env, self.values, self.counter)
                self.entry.entering(person)
                self.counter += 1

            timeout = math.ceil(random.uniform(upper, lower, size=1))
            yield self.env.timeout(timeout)