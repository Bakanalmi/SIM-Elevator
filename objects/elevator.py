from objects import generator
import simpy, math

class Elevator:

    def __init__(self, env, values, ident):
        self.id = ident
        self.env = env

        self.generator = generator.Generator(env, values)
        self.velocity = values.get('elevators').get('velocity')
        self.waiting = values.get('elevators').get('waiting')
        self.capacity = values.get('elevators').get('capacity')
        self.current = 0    # pis actual al qual es troba l'ascensor
        self.upper = True   # True si, i només si, l'ascensor està pujant
        self.floors = {}    # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.over = []      # Individus a l'ascensor

        self.sleep = False
        env.process(self.run())

    def set_floors(self, floors):
        self.floors = floors

    def run(self):
        while True:
            if not self.sleep:
                yield self.env.process(self.leave_elevator())
                
                yield self.env.process(self.free())
                yield self.env.process(self.moving())
            else:
                yield self.env.process(self.do_sleep())

    def discharge(self):
        print('[%d]\tElevator %d is waiting for being empty on floor %s'  % (self.env.now, self.id, self.current))
        
    def charge(self, token):
        if len(self.over) < self.capacity:
            self.over.append(token)
            return True
        
        self.env.process(self.moving())
        return False

    def free(self):
        print('[%d]\tElevator %d is free on floor %s' % (self.env.now, self.id, self.current))

        floor = self.floors[self.current]
        yield self.env.process(floor.arrival(self.id))

    def moving(self):
        next_floor, got = self.closest_floor()
        #while not got:
        if got:
            self.generator.on()
            print('[%d]\tElevator %d goes from %d to %d' % (self.env.now, self.id, self.current, next_floor))
            timeout = abs(next_floor-self.current) * self.velocity
            yield self.env.timeout(timeout)

            self.current = next_floor
            self.generator.off(len(self.over))
        else:
            # There is nowhere to go
            self.sleep = True

    def does_stop(self, floor):
        return floor in self.floors

    def closest_floor(self, it=1):
        next_floor = -1
        if self.upper:
            next_floor = len(self.floors)*2
        
        got = False # Sempre es prioritza conservar el sentit
        selected = self.selected_stops()
        # Quin és el pis més proper en el qual volen arribar les persones a l'interior
        for n, floor in self.floors.items():
            if self.upper and floor.floor < next_floor and floor.floor > self.current:
                # si el pis conserva el sentit i, per tant, es superior a l'actual
                stops = self.floors.keys()
                if floor.waiting_for(stops) or floor.floor in selected:
                    # si el pis conté alguna persona que l'espera o bé, algú de dins hi vol arribar
                    next_floor = floor.floor
                    got = True
            elif floor.floor > next_floor and floor.floor < self.current:
                # si el pis conserva el sentit i, per tant, es inferior a l'actual
                stops = self.floors.keys()
                if floor.waiting_for(stops) or floor.floor in selected:
                    # si el pis conté alguna persona que l'espera o bé, algú de dins hi vol arribar
                    next_floor = floor.floor
                    got = True

        if not got and it < 2:
            self.upper = not self.upper
            next_floor = self.closest_floor(it+1)

        return next_floor, got

    def selected_stops(self):
        selected = []
        for token in self.over:
            selected.append(token.destination)

        return selected

    def leave_elevator(self):
        floor = self.floors[self.current]
        for token in self.over:
            if token.destination == self.current:
                self.over.remove(token)
                floor.entering(token)
                #if self.current == 0:
                #    floor.leaving(token)
                #else:
                #    floor.set_worker(token)

        yield self.env.timeout(self.waiting)
        
    def do_sleep(self):
        print('[%d]\tElevator %d has no where to go' % (self.env.now, self.id))
        none, got = self.closest_floor()
        self.sleep = not got
        yield self.env.timeout(self.waiting)