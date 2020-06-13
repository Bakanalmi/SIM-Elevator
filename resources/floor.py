import simpy

class Floor:

    def __init__(self, env, floor):
        self.env = env
        self.floor = floor  # Pis al qual s'ubica l'oficina
        self.capacity = 120 # Capacitat de l'officina

        self.elevators = {}     # Ascensors els quals arriben al pis
        self.treballant = {}    # Treballadors treballant a l'oficina 
        self.waiting = []       # Treballadors esperant algun ascensor al pis

    def set_elevator(self, ident, elevator):
        self.elevators[ident] = elevator

    def arrival(self, elevator_id):
        yield self.env.timeout(2) # obertura de les portes
        elev = self.elevators[elevator_id]
        
        for token in self.waiting:
            if elev.does_stop(token.destination):
                print('[%d]\tToken %d have entered into elevator %d'  % (self.env.now, token.id, elev.current))
                self.waiting.remove(token)
                elev.charge(token)
