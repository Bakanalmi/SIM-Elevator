from event.Event import Event
from event.Constants import *


class Elevator:

    def __init__(self, values, scheduler, ident):

        self.id = ident
        self.scheduler = scheduler

        self.velocity = values.get('elevators').get('velocity') # Velocitat de l'ascensor
        self.capacity = values.get('elevators').get('capacity') # Capacitat ascensor
        self.currentFloor = 0                                   # Pis actual al qual es troba l'ascensor
        self.floors = {}                                        # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.selectedFloors = {}                                # Pisos seleccionats
        self.peopleIn = []                                      # Individus a l'ascensor
        self.state = State.IDLE                                 # Estats de l'ascensor
        self.downCalls = []                                     # Pisos que han cridat a l'ascensor per baixar
        self.upCalls = None                                     # Si algú ha cridat a l'ascensor des de la planta baixa per pujar
        self.up = False                                         # Ascensor en sentit de pujada

    def setUp(self, floors):
        # Inicialitzem el valor dels pisos als que pot anar l'ascensor
        self.floors = floors
        for key, floor in floors.items():
            self.selectedFloors[key] = False

    def changeStateIDLEToMovement(self, floor):
        if self.currentFloor == floor.floor:
            # Si l'ascensor està en estat IDLE i está en la planta que toca quan el criden deixarà pujar a la gent
            self.state = State.TRANSFER
            self.scheduler.afegirEsdeveniment(Event(floor, self.scheduler.currentTime, EventType.GetPeopleInElevator, self))
        elif self.currentFloor < floor.floor:
            # Si l'ascensor està en estat IDLE i está en una planta inferior quan el criden haurà de canviar de planta
            self.state = State.UP
            self.up = True
            time = self.scheduler.currentTime + (floor.floor - self.currentFloor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))
        else:
            # Si l'ascensor està en estat IDLE i está en una planta superior quan el criden haurà de canviar de planta
            self.state = State.DOWN
            self.up = False
            time = self.scheduler.currentTime + (self.currentFloor - floor.floor) * self.velocity
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))

    def saveUpCall(self, floor):
        # Guarda el número de la planta que l'ha cridat
        self.upCalls = floor.floor

    def saveDownCall(self, floor):
        # Guarda el número de la planta que l'ha cridat
        self.downCalls.append(floor.floor)

    def changeStateTransfer(self):
        if len(self.downCalls) > 0 and self.up:
            # Si l'ascensor ha quedat buit i estava en estat de pujada comprobarà si algú l'havia cridat per abaixar
            self.downCalls.sort(reverse=True)
            firstStop = self.downCalls.pop()
            time = self.scheduler.currentTime
            self.state = State.DOWN
            self.up = False
            if firstStop > self.currentFloor:
                # Primer anirá a buscar la planta més alta
                time += (firstStop - self.currentFloor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[firstStop]))
            else:
                # Primer anirá a buscar la planta més alta
                time += (self.currentFloor - firstStop) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[firstStop]))
            while len(self.downCalls) > 0:
                # Després anirà a les següents en funcion de la més alta
                floor = self.downCalls.pop()
                timeNextStop = time + (firstStop - floor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, timeNextStop, EventType.ChangeFloor, self.floors[floor]))
        elif self.upCalls is not None:
            # Es comproba si l'ascensor te crides per pujar
            if self.currentFloor == self.floors[self.upCalls]:
                # Es comproba si está a la planta que toca en cas de ser així la gent puja
                self.state = State.TRANSFER
                self.scheduler.afegirEsdeveniment(Event(self.floors[self.upCalls], self.scheduler.currentTime, EventType.GetPeopleInElevator, self))
            else:
                # En cas de no estar a la planta que toca canvia de planta
                self.state = State.DOWN
                time = self.scheduler.currentTime + self.currentFloor * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, self.floors[self.upCalls]))
            self.upCalls = None
            self.up = True
        else:
            # Si ningú necessita l'ascensor aquest es posa en estat de repos
            self.state = State.IDLE

    def selectFloor(self, floor):
        if not self.selectedFloors[floor.floor]:
            # Quan puja una persona aquesta selecciona la planta a la que vol anar si ningú l'ha seleccionat amb anterioritat
            print(Colors.OKBLUE, '[%d]\tFloor %d is being selected' % (self.scheduler.currentTime, floor.floor), Colors.ENDC)
            self.selectedFloors[floor.floor] = True
            if self.currentFloor > floor.floor:
                # L'ascensor baixa per anar a buscar el pis
                self.up = False
                self.state = State.DOWN
                time = self.scheduler.currentTime + (self.currentFloor - floor.floor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))
            else:
                # L'ascensor puja per anar a buscar el pis
                self.up = True
                self.state = State.UP
                time = self.scheduler.currentTime + (floor.floor - self.currentFloor) * self.velocity
                self.scheduler.afegirEsdeveniment(Event(self, time, EventType.ChangeFloor, floor))

    def changeFloor(self, floor):
        # L'ascensor canvia de pis
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
