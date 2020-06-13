import simpy, math

class Elevator:

    def __init__(self, env, ident):
        self.id = ident
        self.env = env

        self.velocity = 10  # Temps (en segons) que triga entre pisos consecutius
        self.waiting = 15   # Temps (en segons) d'espera a cada pis
        self.capacity = 12  # Capcitat total de l'ascensor
        self.current = 0    # pis actual al qual es troba l'ascensor
        self.upper = True   # True si, i només si, l'ascensor està pujant
        self.floors = {}    # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.over = []      # Individus a l'ascensor

        env.process(self.run())

    def set_floors(self, floors):
        self.floors = floors

    def run(self):
        while True:
            # L'ascensor està lliure a la planta actual
            yield self.env.process(self.free())
            if len(self.over) > 0:
                yield self.env.process(self.moving())

    def discharge(self):
        print('[%d]\tElevator %d is waiting for being empty on floor %s'  % (self.env.now, self.id, self.current))
        
    def charge(self, token):
        if len(self.over) < self.capacity:
            self.over.append(token)
            return True
        
        return False

    def free(self):
        print('[%d]\tElevator %d is free on floor %s' % (self.env.now, self.id, self.current))

        floor = self.floors[self.current]
        yield self.env.process(floor.arrival(self.id))

    def moving(self):
        next_floor = self.closest_floor()
        print('[%d]\tElevator %d goes from %d to %d' % (self.env.now, self.id, self.current, next_floor))
        timeout = abs(next_floor-self.current) * self.velocity
        yield self.env.timeout(timeout)

        self.current = next_floor

    def does_stop(self, floor):
        return floor in self.floors

    def closest_floor(self):
        next_floor = -1
        if self.upper:
            next_floor = len(self.floors)*2

        for n, floor in self.floors.items():
            if self.upper and floor.floor < next_floor and floor.floor > self.current:
                next_floor = floor.floor
            elif floor.floor > next_floor and floor.floor < self.current:
                next_floor = floor.floor

        return next_floor