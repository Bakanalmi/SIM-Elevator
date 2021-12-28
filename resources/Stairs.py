from event.Constants import *
from event.Event import Event


class Stairs:
    def __init__(self, scheduler, values):
        self.velocity = values.get('stairs').get('velocity')
        self.scheduler = scheduler
        self.floors = {}
        self.peopleIn = []

    def setUp(self, floors):
        for key, floor in floors.items():
            self.floors[key] = floor

    def request(self, person):
        print(Colors.OKCYAN, '[%d]\tToken %d is taking the stairs %d -> %d' % (self.scheduler.currentTime, person.id, person.currentFloor, person.dest), Colors.ENDC)
        self.peopleIn.append(person)
        floor = self.floors[person.dest]
        if person.currentFloor != 0:
            # En cas de que la persona esitgui a una planta diferent de la baixa si agafa les escales serà per marxar
            timeStairs = self.scheduler.currentTime + person.currentFloor * self.velocity
            self.scheduler.afegirEsdeveniment(Event(floor, timeStairs, EventType.OutOfTheBuilding, person))
        else:
            # En cas de que la persona esitgui a la planta baixa si agafa les escales serà per entrar a treballar
            timeStairs = self.scheduler.currentTime + floor.floor * self.velocity
            self.scheduler.afegirEsdeveniment(Event(floor, timeStairs, EventType.StartWorking, person))

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GetStairs:
            self.request(event.entitat)
