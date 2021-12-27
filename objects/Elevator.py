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
        self.peopleIn = []                                      # Individus a l'ascensor
        self.state = State.IDLE                                 # Estats de l'ascensor
        self.downCalls = []
        self.upCalls = None
        self.up = False

    def setUp(self, floors):
        self.floors = floors

    def changeStateIDLEToMovement(self, floor):
        if self.currentFloor == floor.floor:
            self.state = State.TRANSFER
            self.scheduler.afegirEsdeveniment(Event(floor, self.scheduler.currentTime, EventType.GetPeopleInElevator, self))
        elif self.currentFloor < floor.floor:
            self.state = State.UP
            self.up = True
            time = self.scheduler.currentTime + (floor.floor - self.currentFloor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFLoor, floor))
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
            if firstStop.floor > self.currentFloor:
                time += (firstStop.floor - self.currentFloor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(firstStop, time, EventType.GetPeopleInElevator, self))
            elif firstStop.floor < self.currentFloor:
                time += (self.currentFloor - firstStop.floor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(firstStop, time, EventType.GetPeopleInElevator, self))
            else:
                self.scheduler.afegirEsdeveniment(Event(firstStop, time, EventType.GetPeopleInElevator, self))
            while len(self.downCalls) > 0:
                floor = self.downCalls.pop()
                timeNextStop = time + (firstStop - floor.floor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(floor, timeNextStop, EventType.GetPeopleInElevator, self))
        elif self.upCalls:
            if self.currentFloor == self.floors[self.upCalls]:
                self.state = State.TRANSFER
                self.scheduler.afegirEsdeveniment(Event(self.floors[self.upCalls], self.scheduler.currentTime, EventType.GetPeopleInElevator, self))
            else:
                self.state = State.DOWN
                time = self.scheduler.currentTime + self.currentFloor * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self.floors[self.upCalls], time, EventType.GetPeopleInElevator, self))
            self.upCalls = None
            self.up = True
        else:
            self.state = State.IDLE

    def selectFloor(self, floor):
        print('[%d]\tFloor %d is being selected.' % (self.scheduler.currentTime, floor.floor))
        if self.currentFloor > floor.floor:
            self.up = False
            time = self.scheduler.currentTime + (self.currentFloor - floor.floor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(floor, time, EventType.GetPeopleOutElevator, self))
        else:
            self.up = True
            time = self.scheduler.currentTime + (floor.floor - self.currentFloor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(floor, time, EventType.GetPeopleOutElevator, self))

    def changeFloor(self, floor):
        self.currentFloor = floor.floor
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
