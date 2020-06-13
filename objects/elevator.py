import simpy

class Elevator:
    def __init__(self, env):
        self.env = env
        self.env.process(self.run())

        self.velocity = 10  # Temps (en segons) que triga entre pisos consecutius
        self.module = -1    # Només para en pisos tals que #pis%2 == module; module = -1 implica para a totes les plantes
        self.current = 0    # pis actual al qual es troba l'ascensor
        self.upper = True   # True si, i només si, l'ascensor està pujant
        self.stops = []     # Pisos als qual s'espera que pari l'ascensor
        self.calls = []     # Pisos des dels quals s'ha trucat l'ascensor

    def run(self):
        while True:
            print('Start parking at %d' % self.env.now)
            parking_duration = 5
            yield self.env.timeout(parking_duration)

            print('Start driving at %d' % self.env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def discharge(self):
        print('[%d]\tElevator is waiting for being empty on floor %s'  % (self.env.now, self.current))
        
    def charge(self):
        print('[%d]\tElevator is waiting for being full on floor %s' % (self.env.now, self.current))

    def free(self):
        print('[%d]\tElevator becomes free on floor %s' % (self.env.now, self.current))

    def moving(self):
        print('[%d]\tElevator is moving from floor %d, to %d' % (self.env.now, self.current, self.current))