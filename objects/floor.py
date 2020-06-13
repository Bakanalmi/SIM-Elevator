import simpy

class Floor:

    def __init__(self, env, floor):
        self.env = env
        self.floor = floor  # Pis al qual s'ubica

        self.elevators = {}     # Ascensors els quals arriben al pis
        self.working = []    # Treballadors treballant a l'oficina 
        self.waiting = []       # Treballadors esperant algun ascensor al pis

    def set_elevator(self, ident, elevator):
        self.elevators[ident] = elevator

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
        print('[%d]\tToken %d destination is floor %d'  % (self.env.now, token.id, token.office_floor))
        self.waiting.append(token)

    def set_worker(self, token):
        print('[%d]\tToken %d starts working on floor %d'  % (self.env.now, token.id, token.office_floor))
        self.working.append(token)

    def leaving(self, token):
        print('[%d]\tToken %d is leaving at home'  % (self.env.now, token.id))