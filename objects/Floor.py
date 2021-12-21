from event.Constants import *
from event.Event import Event
import time


class Floor:

    def __init__(self, scheduler, values, floor):

        self.floor = floor   # Pis actual
        self.elevators = {}  # Ascensors del pis
        self.personWaiting = []    # Gent esperant
        self.personWorking = []
        self.home = None
        self.scheduler = scheduler
        self.workingTime = values.get('time').get('work')

        self.metrics = None

    def set_elevator(self, ident, elevator):
        self.elevators[ident] = elevator

    def set_stairs(self, stairs):
        self.stairs = stairs

    def searchPerson(self, personId):
        for person in self.personWorking:
            if person['id'] == personId:
                return person

    def startWorking(self, person):
        print('[%d]\tToken %d is start working.' % (self.scheduler.currentTime, person.id))
        self.personWorking.append(person)
        workingTime = self.scheduler.currentTime + self.workingTime * 3600
        self.scheduler.afegirEsdeveniment(Event(self, workingTime, EventType.FinishWorking, person))

    def finishWorking(self, person):
        print('[%d]\tToken %d finish working.' % (self.scheduler.currentTime, person.id))
        self.personWorking.remove(person)
        if person.walker:
            self.scheduler.afegirEsdeveniment(Event(self.stairs, self.scheduler.currentTime, EventType.GetStairs, person))
        else:
            self.scheduler.afegirEsdeveniment(Event(self.elevators.get(0), self.scheduler.currentTime, EventType.GetElevator, person))

    def tractarEsdeveniment(self, event):
        if event.type == EventType.StartWorking:
            self.startWorking(event.entitat)

        if event.type == EventType.FinishWorking:
            self.finishWorking(event.entitat)
