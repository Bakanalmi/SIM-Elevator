from event.Constants import *
from event.Event import Event


class Floor:

    def __init__(self, scheduler, values, n_floor):

        self.floor = n_floor                                # Pis actual
        self.elevators = {}                                 # Ascensors del pis
        self.peopleWaitingPar = []                          # Gent esperant
        self.peopleWaitingImpar = []                        # Gent esperant
        self.peopleWaiting = []                             # Gent esperant
        self.peopleWorking = []
        self.home = None
        self.scheduler = scheduler
        self.workingTime = values.get('time').get('work')

        self.metrics = None

    def set_elevator(self, ident, elevator):
        self.elevators[ident] = elevator

    def set_stairs(self, stairs):
        self.stairs = stairs

    def searchPerson(self, personId):
        for person in self.peopleWorking:
            if person['id'] == personId:
                return person

    def startWorking(self, elevator):
        elevator.currentFloor = self.floor
        for person in elevator.peopleIn:
            if person.dest == self.floor:
                print('[%d]\tToken %d starts working.' % (self.scheduler.currentTime, person.id))
                self.peopleWorking.append(person)
                workingTime = self.scheduler.currentTime + self.workingTime * 3600
                self.scheduler.afegirEsdeveniment(Event(self, workingTime, EventType.FinishWorking, person))

        for person in self.peopleWorking:
            if person in elevator.peopleIn:
                elevator.peopleIn.remove(person)

        if len(elevator.peopleIn) == 0:
            self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.Empty, None))

    def finishWorking(self, person):
        print('[%d]\tToken %d finish working.' % (self.scheduler.currentTime, person.id))
        self.peopleWorking.remove(person)
        if person.walker:
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            if len(self.peopleWaiting) > 0:
                self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.CallDown, self))
            self.peopleWaiting.append(person)

    def getPeopleWaitingInTheElevator(self, elevator):
        elevator.currentFloor = self.floor
        if self.floor != 0:
            while len(self.peopleWaiting):
                person = self.peopleWaiting.pop()
                print('[%d]\tToken %d get in the elevator.' % (self.scheduler.currentTime, person.id))
                elevator.peopleIn.append(person)
                self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(0)))
        else:
            if elevator.id % 2 == 0:
                while len(self.peopleWaitingPar):
                    person = self.peopleWaitingPar.pop()
                    print('[%d]\tToken %d get in the elevator.' % (self.scheduler.currentTime, person.id))
                    elevator.peopleIn.append(person)
                    self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(person.dest)))
            else:
                while len(self.peopleWaitingImpar):
                    person = self.peopleWaitingImpar.pop()
                    print('[%d]\tToken %d get in the elevator.' % (self.scheduler.currentTime, person.id))
                    elevator.peopleIn.append(person)
                    self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(person.dest)))

    def personGetInTheBuilding(self, person):
        if person.walker:
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            if person.dest % 2 == 0:
                if len(self.peopleWaitingPar) == 0:
                    print('[%d]\tToken %d Call the elevator 0.' % (self.scheduler.currentTime, person.id))
                    self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.CallUp, self))
                self.peopleWaitingPar.append(person)
            else:
                if len(self.peopleWaitingImpar) == 0:
                    print('[%d]\tToken %d Call the elevator 1' % (self.scheduler.currentTime, person.id))
                    self.scheduler.afegirEsdeveniment(Event(self.elevators.get(1), self.scheduler.currentTime, EventType.CallUp, self))
                self.peopleWaitingImpar.append(person)

    def exitBuilding(self, elevator):
        peopleHome = []
        for person in elevator.peopleIn:
            peopleHome.append(person)
            self.scheduler.afegirEsdeveniment(Event(self.home, self.scheduler.currentTime, EventType.DeletePerson, person))
        for person in peopleHome:
            if person in elevator.peopleIn:
                elevator.peopleIn.remove(person)

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GetPeopleOutElevator:
            if self.floor == 0:
                self.exitBuilding(event.entitat)
            else:
                self.startWorking(event.entitat)

        elif event.type == EventType.FinishWorking:
            self.finishWorking(event.entitat)

        elif event.type == EventType.GetPeopleInElevator:
            self.getPeopleWaitingInTheElevator(event.entitat)

        elif event.type == EventType.EnterBuilding:
            self.personGetInTheBuilding(event.entitat)
