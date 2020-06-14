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
        print('[%d]\tToken %d destination is floor %d'  % (self.env.now, token.id, token.destination))
        if token.walker:
            self.env.process(self.stairs.request(token))
        else:
            self.waiting.append(token)

    def set_worker(self, token):
        self.env.process(self.office.request(token))
        token.destination = 0
        self.entering(token)

    def leaving(self, token):
        if self.floor == 0 and self.home != None:
            self.home.delete_token(token)