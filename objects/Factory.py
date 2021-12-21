from event.Constants import *
from entities import Person
from event.Event import Event
import random


class Token:
    def __init__(self, scheduler, entry, values):
        self.counter = 0
        self.scheduler = scheduler
        self.entry = entry
        self.values = values
        self.MAX = (values.get('environment').get('n_floors') * values.get('environment').get('cap_floor'))

        self.home = 0

    def newToken(self):
        if self.MAX > self.counter:
            time = self.scheduler.currentTime + random.randint(1, 60)
            self.scheduler.eventList.append(Event(self.scheduler, time, EventType.GeneratePeople, None))
            for iterator in range(1, 5):
                person = Person.Person(self.values, self.counter)
                print('[%d]\tToken %d is being generated' % (self.scheduler.currentTime, person.id))
                self.scheduler.eventList.append(Event(self.entry, self.scheduler.currentTime, EventType.EnterBuilding, person))
                self.counter += 1

    def deleteToken(self, token):
        print('[%d]\tToken %d is leaving at home' % (self.scheduler.currentTime, token.id))
        self.home += 1
        del token

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GeneratePeople:
            self.newToken()
        elif event.type == EventType.DeletePerson:
            self.deleteToken(event.entitat)
