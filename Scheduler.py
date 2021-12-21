from event.Constants import *
from event.Event import Event
from objects import Elevator, factory, Floor as obj_floor
from resources import Stairs as res_stairs
import bisect
import time


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
        if (event.type == EventType.SimulationStart):
            self.factory.simulationStart()

    def createModel(self):
        self.createBuild()
        self.createStairs()
        self.createStairs()

    def createBuild(self):
        # Creació dels pisos i classificació entre parells i senars
        for n_floor in range(0, self.values.get('environment').get('n_floors') + 1):
            floor = obj_floor.Floor(self, self.values, n_floor)

            if n_floor == 0 or n_floor % 2 == 0:
                self.floors_parell[n_floor] = floor
            if n_floor == 0 or n_floor % 2 != 0:
                self.floors_senars[n_floor] = floor

            if n_floor == 0:
                self.factory = factory.Token(floor, self.values)
                floor.home = self.factory

    def createStairs(self):
        # Creació de l'escala
        self.stairs = res_stairs.Stairs(self, self.values)
        self.stairs.setUp(self.floors_parell)
        self.stairs.setUp(self.floors_senars)

    def createElevator(self):
        # Creació dels ascensors i assignació dels pisos disponibles
        for n_elev in range(0, self.values.get('environment').get('n_elevator')):
            self.elev = Elevator.Elevator(self.values, n_elev)
            if n_elev % 2 == 0:
                self.elev.setUp(self.floors_parell)
                for key in self.floors_parell:
                    self.floors_parell[key].set_elevator(n_elev, self.elev)
                    self.floors_parell[key].set_stairs(self.stairs)
            else:
                self.elev.setUp(self.floors_senars)
                for key in self.floors_senars:
                    self.floors_senars[key].set_elevator(n_elev, self.elev)
                    self.floors_senars[key].set_stairs(self.stairs)