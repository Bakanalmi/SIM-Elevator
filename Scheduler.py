from event.Constants import *
from event.Event import Event
from objects import Elevator, Factory, Floor
from resources import Stairs
import bisect


class ElevatorSimulation:
    eventList = []
    floors_parell = {}
    floors_senars = {}
    currentTime = 0

    def __init__(self, values):
        self.simulationStart = Event(self, 0, EventType.SimulationStart, None)
        self.eventList.append(self.simulationStart)
        self.values = values

        self.createModel()

    def run(self):
        while len(self.eventList) > 0:
            # recuperem event simulacio
            event = self.eventList.pop(0)
            self.currentTime = event.tid
            # deleguem l'accio a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # tambe podriem delegar l'accio a un altre objecte
            event.objekt.tractarEsdeveniment(event)

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)

    def tractarEsdeveniment(self, event):
        if event.type == EventType.SimulationStart:
            self.eventList.append(Event(self.factory, self.currentTime, EventType.GeneratePeople, None))

    def createModel(self):
        self.createBuild()
        self.createStairs()
        self.createElevator()

    def createBuild(self):
        # Creació dels pisos i classificació entre parells i senars
        for n_floor in range(0, 10):
            floor = Floor.Floor(self, self.values, n_floor)

            if n_floor == 0 or n_floor % 2 == 0:
                self.floors_parell[n_floor] = floor
            if n_floor == 0 or n_floor % 2 != 0:
                self.floors_senars[n_floor] = floor

            if n_floor == 0:
                self.factory = Factory.Token(self, floor, self.values)
                floor.home = self.factory

    def createStairs(self):
        # Creació de l'escala
        self.stairs = Stairs.Stairs(self, self.values)
        self.stairs.setUp(self.floors_parell)
        self.stairs.setUp(self.floors_senars)

    def createElevator(self):
        # Creació dels ascensors i assignació dels pisos disponibles
        elev = Elevator.Elevator(self.values, self, 0)
        elev.setUp(self.floors_parell)
        for key in self.floors_parell:
            self.floors_parell[key].set_elevator(0, elev)
            self.floors_parell[key].set_stairs(self.stairs)
        elev = Elevator.Elevator(self.values, self, 1)
        elev.setUp(self.floors_senars)
        for key in self.floors_senars:
            if key == 0:
                self.floors_senars[key].set_elevator(1, elev)
            else:
                self.floors_senars[key].set_elevator(0, elev)
            self.floors_senars[key].set_stairs(self.stairs)
