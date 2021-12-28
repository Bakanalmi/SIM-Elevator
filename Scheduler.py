from event.Constants import *
from event.Event import Event
from objects import Elevator, Factory, Floor
from resources import Stairs
from metrics import Simplot
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
        self.metrics.show()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)

    def tractarEsdeveniment(self, event):
        if event.type == EventType.SimulationStart:
            self.eventList.append(Event(self.metrics, self.currentTime, EventType.UpdateMetrics, None))
            self.eventList.append(Event(self.factory, self.currentTime, EventType.GeneratePeople, None))

    def createModel(self):
        self.createBuild()
        self.createStairs()
        self.createElevator()
        self.createMetrics()

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
        self.elevPar = Elevator.Elevator(self.values, self, 0)
        self.elevPar.setUp(self.floors_parell)
        for key in self.floors_parell:
            self.floors_parell[key].set_elevator(0, self.elevPar)
            self.floors_parell[key].set_stairs(self.stairs)
        self.elevImPar = Elevator.Elevator(self.values, self, 1)
        self.elevImPar.setUp(self.floors_senars)
        for key in self.floors_senars:
            if key == 0:
                self.floors_senars[key].set_elevator(1, self.elevImPar)
            else:
                self.floors_senars[key].set_elevator(0, self.elevImPar)
            self.floors_senars[key].set_stairs(self.stairs)

    def createMetrics(self):
        self.metrics = Simplot.Metrics(self, self.values, 'elevators strategy')
        self.metrics.set_resource_floors(self.floors_senars)
        self.metrics.set_resource_floors(self.floors_parell)
        self.metrics.set_resource_elevators(self.elevPar)
        self.metrics.set_resource_elevators(self.elevImPar)
