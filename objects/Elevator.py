from event.Event import Event
from event.Constants import *


class Elevator:

    def __init__(self, values, scheduler, ident):

        self.id = ident
        self.scheduler = scheduler

        self.velocity = values.get('elevators').get('velocity')
        self.capacity = values.get('elevators').get('capacity')
        self.currentFloor = 0                                   # pis actual al qual es troba l'ascensor
        self.floors = {}                                        # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.selectedFloors = {}
        self.peopleIn = []                                      # Individus a l'ascensor
        self.state = State.IDLE                                 # Estats de l'ascensor
        self.downCalls = []
        self.upCalls = None
        self.up = False

    def setUp(self, floors):
        self.floors = floors
        for key, floor in floors.items():
            self.selectedFloors[key] = False

    def changeStateIDLEToMovement(self, floor):
        if self.currentFloor == floor.floor:
            self.state = State.TRANSFER
            self.scheduler.afegirEsdeveniment(Event(floor, self.scheduler.currentTime, EventType.GetPeopleInElevator, self))
        elif self.currentFloor < floor.floor:
            self.state = State.UP
            self.up = True
            time = self.scheduler.currentTime + (floor.floor - self.currentFloor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))
        else:
            self.state = State.DOWN
            self.up = False
            time = self.scheduler.currentTime + (self.currentFloor - floor.floor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))

    def saveUpCall(self, floor):
        self.upCalls = floor.floor

    def saveDownCall(self, floor):
        self.downCalls.append(floor.floor)

    def changeStateTransfer(self):
        if len(self.downCalls) > 0 and self.up:
            self.downCalls.sort(reverse=True)
            firstStop = self.downCalls.pop()
            time = self.scheduler.currentTime
            self.state = State.DOWN
            self.up = False
            if firstStop > self.currentFloor:
                time += (firstStop - self.currentFloor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[firstStop]))
            elif firstStop < self.currentFloor:
                time += (self.currentFloor - firstStop) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[firstStop]))
            else:
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[firstStop]))
            while len(self.downCalls) > 0:
                floor = self.downCalls.pop()
                timeNextStop = time + (firstStop - floor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, timeNextStop, EventType.ChangeFloor, self.floors[floor]))
        elif self.upCalls is not None:
            if self.currentFloor == self.floors[self.upCalls]:
                self.state = State.TRANSFER
                self.scheduler.afegirEsdeveniment(Event(self, self.scheduler.currentTime, EventType.ChangeFloor, self.floors[self.upCalls]))
            else:
                self.state = State.DOWN
                time = self.scheduler.currentTime + self.currentFloor * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[self.upCalls]))
            self.upCalls = None
            self.up = True
        else:
            self.state = State.IDLE

    def selectFloor(self, floor):
        if not self.selectedFloors[floor.floor]:
            print(Colors.OKBLUE, '[%d]\tFloor %d is being selected' % (self.scheduler.currentTime, floor.floor), Colors.ENDC)
            self.selectedFloors[floor.floor] = True
            if self.currentFloor > floor.floor:
                self.up = False
                self.state = State.DOWN
                time = self.scheduler.currentTime + (self.currentFloor - floor.floor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))
            else:
                self.up = True
                self.state = State.UP
                time = self.scheduler.currentTime + (floor.floor - self.currentFloor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))

    def changeFloor(self, floor):
        self.currentFloor = floor.floor
        print(Colors.OKBLUE, '[%d]\tElevator %d arrived to the floor %d' % (self.scheduler.currentTime, self.id, self.currentFloor), Colors.ENDC)
        self.state = State.TRANSFER
        self.scheduler.afegirEsdeveniment(Event(floor, self.scheduler.currentTime, EventType.GetPeopleOutElevator, self))
        self.scheduler.afegirEsdeveniment(Event(floor, self.scheduler.currentTime, EventType.GetPeopleInElevator, self))

    def tractarEsdeveniment(self, event):
        if event.type == EventType.CallUp:
            if self.state == State.IDLE:
                self.changeStateIDLEToMovement(event.entitat)
            else:
                self.saveUpCall(event.entitat)

        elif event.type == EventType.ChangeFloor:
            self.changeFloor(event.entitat)

        elif event.type == EventType.CallDown:
            if self.state == State.IDLE:
                self.changeStateIDLEToMovement(event.entitat)
            else:
                self.saveDownCall(event.entitat)

        elif event.type == EventType.Empty:
            self.changeStateTransfer()

        elif event.type == EventType.SelectFloor:
            self.selectFloor(event.entitat)
