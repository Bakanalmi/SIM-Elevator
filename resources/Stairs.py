from event.Constants import *
from event.Event import Event


class Stairs:
    def __init__(self, scheduler, values):
        self.velocity = values.get('stairs').get('velocity')
        self.scheduler = scheduler
        self.floors = {}

    def setUp(self, floors):
        for key, floor in floors.items():
            self.floors[key] = floor

    def request(self, person):
        print(Colors.OKCYAN, '[%d]\tToken %d is taking the stairs' % (self.scheduler.currentTime, person.id), Colors.ENDC)
        floor = self.floors[person.dest]
        timeStairs = self.scheduler.currentTime + floor.floor * self.velocity
        self.scheduler.afegirEsdeveniment(Event(floor, timeStairs, EventType.StartWorking, person))

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GetStairs:
            self.request(event.entitat)
