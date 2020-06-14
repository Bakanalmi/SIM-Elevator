from resources import stairs, office
import simpy

class Floor:

    def __init__(self, env, values, floor):
        self.env = env
        self.floor = floor  # Pis al qual s'ubica

        self.elevators = {}     # Ascensors els quals arriben al pis
        self.waiting = []       # Treballadors esperant algun ascensor al pis
        self.home = None

        if self.floor > 0:
            self.office = office.Office(env, values, self)

        self.metrics = None
        
    def set_elevator(self, ident, elevator):
        self.elevators[ident] = elevator

    def set_stairs(self, stairs):
        self.stairs = stairs

    def arrival(self, elevator_id):
        yield self.env.timeout(2) # obertura de les portes
        elev = self.elevators[elevator_id]
        
        succeed = True
        for token in self.waiting:
            if not succeed:
                break
            
            print("ELEV DOES STOP: ", token.destination, " VERERDICT: ", elev.does_stop(token.destination))
            if elev.does_stop(token.destination):
                succeed = elev.charge(token)
                if succeed:
                    print('[%d]\tToken %d goes to elevator %d'  % (self.env.now, token.id, elev.id))
                    self.waiting.remove(token)

    def waiting_for(self, floors):
        waiting = False
        for token in self.waiting:
            waiting = waiting or token.destination in floors

        return waiting

    def entering(self, token):
        token.current = self.floor
        if token.destination == self.floor:
            if self.metrics != None:
                arrival = self.env.now
                entry = token.latest
                self.metrics.waiting(arrival-entry)

            print('[%d]\tToken %d arrived at floor %d'  % (self.env.now, token.id, self.floor))
            if self.floor == 0:
                self.leaving(token)
            else:
                self.env.process(self.office.request(token))

        else:
            print('[%d]\tToken %d destination is floor %d'  % (self.env.now, token.id, token.destination))
            if token.walker:
                self.env.process(self.stairs.request(token))
            else:
                self.waiting.append(token)

    def leaving(self, token):
        if self.floor == 0 and self.home != None:
            self.home.delete_token(token)