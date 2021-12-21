from resources import stairs, office
import simpy


class Floor:

    def __init__(self, floor):

        self.floor = floor   # Pis actual
        self.elevators = {}  # Ascensors del pis
        self.personWaiting = []    # Gent esperant
        self.home = None

        self.metrics = None

    def set_elevator(self, ident, elevator):
        self.elevators[ident] = elevator

    def set_stairs(self, stairs):
        self.stairs = stairs


    def eleArriv(self, ident):
        ele = self.elevators[ident]

        error = False

        for person in self.personWaiting:
            if error:
                break

            if ele.stop_floor(person.desti):
                personUp = ele.transferencia(person)
                if personUp:
                    self.personWaiting.remove(person)






    def waiting_for(self, floors):
        waiting = False
        for person in self.waiting:
            waiting = waiting or person.dest in floors

        return waiting

    def floorArrival(self, person):
        person.currentFloor = self.floor
        if person.dest == self.floor:
            if self.metrics != None:
                #poner tiempo y metrics
            if self.floor == 0:
                home = True
                self.leaving(person, home)
            else:
                home = False
                self.leaving(person, home)



    def leaving(self, person, home):
        if self.floor == 0 and home:
            self.home.delete_token(person)

        elif self.floor == 0 and not home:
            self.personWaiting.append(person)
