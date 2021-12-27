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

    def finishWorking(self, person):
        print(Colors.OKGREEN, '[%d]\tToken %d finish working' % (self.scheduler.currentTime, person.id), Colors.ENDC)
        self.peopleWorking.remove(person)
        if person.walker:
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            if len(self.peopleWaiting) == 0:
                self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.CallDown, self))
            self.peopleWaiting.append(person)

    def getPeopleWaitingInTheElevator(self, elevator):
        elevator.currentFloor = self.floor
        if self.floor != 0:
            while len(self.peopleWaiting):
                person = self.peopleWaiting.pop()
                print(Colors.OKGREEN, '[%d]\tToken %d get in the elevator' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                elevator.peopleIn.append(person)
                self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(0)))
        else:
            if elevator.id % 2 == 0:
                while len(self.peopleWaitingPar):
                    person = self.peopleWaitingPar.pop()
                    print(Colors.OKGREEN, '[%d]\tToken %d get in the elevator' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    elevator.peopleIn.append(person)
                    self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(person.dest)))
            else:
                while len(self.peopleWaitingImpar):
                    person = self.peopleWaitingImpar.pop()
                    print(Colors.OKGREEN, '[%d]\tToken %d get in the elevator' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    elevator.peopleIn.append(person)
                    self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(person.dest)))

    def personGetInTheBuilding(self, person):
        if person.walker:
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            if person.dest % 2 == 0:
                if len(self.peopleWaitingPar) == 0:
                    print(Colors.OKGREEN, '[%d]\tToken %d Call the elevator 0' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.CallUp, self))
                self.peopleWaitingPar.append(person)
            else:
                if len(self.peopleWaitingImpar) == 0:
                    print(Colors.OKGREEN, '[%d]\tToken %d Call the elevator 1' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    self.scheduler.afegirEsdeveniment(Event(self.elevators.get(1), self.scheduler.currentTime, EventType.CallUp, self))
                self.peopleWaitingImpar.append(person)

    def peopleGetOutOfTheElevator(self, elevator):
        peopleOut = []
        if self.floor == 0:
            elevator.selectedFloors[self.floor] = False
            for person in elevator.peopleIn:
                peopleOut.append(person)
                self.scheduler.afegirEsdeveniment(Event(self.home, self.scheduler.currentTime, EventType.DeletePerson, person))
        else:
            elevator.selectedFloors[self.floor] = False
            elevator.currentFloor = self.floor
            for person in elevator.peopleIn:
                if person.dest == self.floor:
                    print(Colors.OKGREEN, '[%d]\tToken %d starts working' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    self.peopleWorking.append(person)
                    peopleOut.append(person)
                    workingTime = self.scheduler.currentTime + self.workingTime * 3600
                    self.scheduler.afegirEsdeveniment(Event(self, workingTime, EventType.FinishWorking, person))
        for person in peopleOut:
            if person in elevator.peopleIn:
                elevator.peopleIn.remove(person)
        if len(elevator.peopleIn) == 0:
            self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.Empty, None))

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GetPeopleOutElevator:
            self.peopleGetOutOfTheElevator(event.entitat)

        elif event.type == EventType.FinishWorking:
            self.finishWorking(event.entitat)

        elif event.type == EventType.GetPeopleInElevator:
            self.getPeopleWaitingInTheElevator(event.entitat)

        elif event.type == EventType.EnterBuilding:
            self.personGetInTheBuilding(event.entitat)
