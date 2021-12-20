from event.Constants import *
from event.Event import Event
from objects import elevator, factory, floor as obj_floor
from resources import stairs as res_stairs
from metrics import simplot


class ElevatorSimulation:
    eventList = []
    floors_parell = {}
    floors_senars = {}

    def __init__(self, values):
        self.simulationStart = Event(self, 0, EventType.SimulationStart, None)
        self.eventList.append(self.simulationStart)
        self.values = values

        # Creació de l'escala
        stairs = res_stairs.Stairs(values)
        stairs.set_floors(self.floors_parell)
        stairs.set_floors(self.floors_senars)

        # Creació dels ascensors i assignació dels pisos disponibles
        for n_elev in range(0, values.get('environment').get('n_elevator')):
            elev = elevator.Elevator(values, n_elev)
            if n_elev % 2 == 0:
                elev.set_floors(self.floors_parell)
                for key in self.floors_parell:
                    self.floors_parell[key].set_elevator(n_elev, elev)
                    self.floors_parell[key].set_stairs(stairs)
            else:
                elev.set_floors(self.floors_senars)
                for key in self.floors_senars:
                    self.floors_senars[key].set_elevator(n_elev, elev)
                    self.floors_senars[key].set_stairs(stairs)

    def createModel(self):
        # Creació dels pisos i classificació entre parells i senars
        for n_floor in range(0, self.values.get('environment').get('n_floors') + 1):
            floor = obj_floor.Floor(self.values, n_floor)

            if n_floor == 0 or n_floor % 2 == 0:
                self.floors_parell[n_floor] = floor
            if n_floor == 0 or n_floor % 2 != 0:
                self.floors_senars[n_floor] = floor

            if n_floor == 0:
                floor.home = factory.Token(floor, self.values)
