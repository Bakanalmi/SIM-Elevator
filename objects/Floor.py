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

    def getPeopleFromStairs(self, person):

        print(Colors.OKGREEN, '[%d]\tToken %d starts working at floor %d' % (self.scheduler.currentTime, person.id, self.floor), Colors.ENDC)
        person.currentFloor = self.floor
        self.stairs.peopleIn.remove(person)
        self.peopleWorking.append(person)
        workingTime = self.scheduler.currentTime + self.workingTime * 3600
        self.scheduler.afegirEsdeveniment(Event(self, workingTime, EventType.FinishWorking, person))

    def finishWorking(self, person):
        # La persona acaba la seva jornada laboral
        print(Colors.OKGREEN, '[%d]\tToken %d finish working' % (self.scheduler.currentTime, person.id), Colors.ENDC)
        self.peopleWorking.remove(person)
        person.dest = 0
        if person.walker:
            # Si la persona li agrada anara per les escales va a buscar les escales
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            # Si la persona li agrada anara amb ascensor va a buscar l'ascensor
            if len(self.peopleWaiting) == 0:
                # si no hi ha ningú a la cua crida a l'ascensor
                self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.CallDown, self))
            self.peopleWaiting.append(person)

    def getPeopleWaitingInTheElevator(self, elevator):
        # Quan l'ascensor arriba al pis la gent que està esperant entren dintre
        elevator.currentFloor = self.floor
        if self.floor != 0:
            # Aqui es diferencia entre la planta 0, ja que té una cua per cada ascensor, i les altres plantes que tenen una cua
            while len(self.peopleWaiting) > 0 and len(elevator.peopleIn) <= elevator.capacity:
                # La gent entra a l'ascensor
                person = self.peopleWaiting.pop(0)
                print(Colors.OKGREEN, '[%d]\tToken %d gets in the elevator %d' % (self.scheduler.currentTime, person.id, elevator.id), Colors.ENDC)
                elevator.peopleIn.append(person)
                self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(0)))
            if len(self.peopleWaiting) and len(elevator.peopleIn) >= elevator.capacity:
                elevator.downCalls.append(self.floor)
        else:
            # Aqui es diferencia entre la planta 0, ja que té una cua per cada ascensor, i les altres plantes que tenen una cua
            if elevator.id % 2 == 0:
                # Si la persona está a la planta baixa i vol anar a un pis par es posarà en la cua de l'ascensor par
                while len(self.peopleWaitingPar) > 0 and len(elevator.peopleIn) <= elevator.capacity:
                    # La gent entra a l'ascensor
                    person = self.peopleWaitingPar.pop(0)
                    print(Colors.OKGREEN, '[%d]\tToken %d gets in the elevator %d' % (self.scheduler.currentTime, person.id, elevator.id), Colors.ENDC)
                    elevator.peopleIn.append(person)
                    self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(person.dest)))
                if len(self.peopleWaitingPar) and len(elevator.peopleIn) >= elevator.capacity:
                    elevator.upCalls = self.floor
            else:
                # Si la persona está a la planta baixa i vol anar a un pis impar es posarà en la cua de l'ascensor impar
                while len(self.peopleWaitingImpar) > 0 and len(elevator.peopleIn) <= elevator.capacity:
                    # La gent entra a l'ascensor
                    person = self.peopleWaitingImpar.pop(0)
                    print(Colors.OKGREEN, '[%d]\tToken %d gets in the elevator %d' % (self.scheduler.currentTime, person.id, elevator.id), Colors.ENDC)
                    elevator.peopleIn.append(person)
                    self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.SelectFloor, elevator.floors.get(person.dest)))
                if len(self.peopleWaitingImpar) > 0 and len(elevator.peopleIn) >= elevator.capacity:
                    elevator.upCalls = self.floor

    def personGetInTheBuilding(self, person):
        # Entra gent a l'edifici
        if person.walker:
            # Si li agraden les escales va a buscar les escales
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            # Si no li agraden les escales va a buscar les va a buscar l'ascensor
            if person.dest % 2 == 0:
                # Si va a un pis par espera en la cua de l'ascensor par
                if len(self.peopleWaitingPar) == 0:
                    # Si no hi ha ningú a la cua crida a l'ascensor
                    print(Colors.OKGREEN, '[%d]\tToken %d Call the elevator 0' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.CallUp, self))
                self.peopleWaitingPar.append(person)
            else:
                # Si va a un pis impar espera en la cua de l'ascensor impar
                if len(self.peopleWaitingImpar) == 0:
                    # Si no hi ha ningú a la cua crida a l'ascensor
                    print(Colors.OKGREEN, '[%d]\tToken %d Call the elevator 1' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                    self.scheduler.afegirEsdeveniment(Event(self.elevators.get(1), self.scheduler.currentTime, EventType.CallUp, self))
                self.peopleWaitingImpar.append(person)

    def peopleGetOutOfTheElevator(self, elevator):
        # Quan s'arriba al pis la gent baixa de l'ascensor
        peopleOut = []
        if self.floor == 0:
            # Si arriben a la planta baixa será per marxar a casa
            elevator.selectedFloors[self.floor] = False
            for person in elevator.peopleIn:
                person.currentFloor = self.floor
                peopleOut.append(person)
                self.scheduler.afegirEsdeveniment(Event(self.home, self.scheduler.currentTime, EventType.DeletePerson, person))
        else:
            # Si arriben a una l'altre planta que no sigui la baixa serà per començar a treballar
            elevator.selectedFloors[self.floor] = False
            elevator.currentFloor = self.floor
            for person in elevator.peopleIn:
                if person.dest == self.floor:
                    print(Colors.OKGREEN, '[%d]\tToken %d starts working at floor %d' % (self.scheduler.currentTime, person.id, self.floor), Colors.ENDC)
                    person.currentFloor = self.floor
                    self.peopleWorking.append(person)
                    peopleOut.append(person)
                    workingTime = self.scheduler.currentTime + self.workingTime * 3600
                    self.scheduler.afegirEsdeveniment(Event(self, workingTime, EventType.FinishWorking, person))
        for person in peopleOut:
            if person in elevator.peopleIn:
                elevator.peopleIn.remove(person)
        if len(elevator.peopleIn) == 0:
            # Si l'ascensor està buit canviarà el seu estat
            self.scheduler.afegirEsdeveniment(Event(elevator, self.scheduler.currentTime, EventType.Empty, None))

    def getOutOfTheStairs(self, person):
        person.currentFloor = self.floor
        self.stairs.peopleIn.remove(person)
        self.scheduler.afegirEsdeveniment(Event(self.home, self.scheduler.currentTime, EventType.DeletePerson, person))

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GetPeopleOutElevator:
            self.peopleGetOutOfTheElevator(event.entitat)

        elif event.type == EventType.OutOfTheBuilding:
            self.getOutOfTheStairs(event.entitat)

        elif event.type == EventType.StartWorking:
            self.getPeopleFromStairs(event.entitat)

        elif event.type == EventType.FinishWorking:
            self.finishWorking(event.entitat)

        elif event.type == EventType.GetPeopleInElevator:
            self.getPeopleWaitingInTheElevator(event.entitat)

        elif event.type == EventType.EnterBuilding:
            self.personGetInTheBuilding(event.entitat)
