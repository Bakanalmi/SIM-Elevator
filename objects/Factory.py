from event.Constants import *
from entities import Person
from event.Event import Event
from numpy import random
import math


class Token:
    def __init__(self, scheduler, entry, values):
        self.counter = 0
        self.scheduler = scheduler
        self.entry = entry
        self.values = values
        self.MAX = values.get('environment').get('cap_building')
        self.loc = self.values.get('arrival').get('loc')
        self.scale = self.values.get('arrival').get('scale')

        self.upper = self.values.get('arrival').get('upper')
        self.lower = self.values.get('arrival').get('lower')

        self.home = 0

    def newToken(self):
        if self.MAX > self.counter:
            random.seed(self.counter % 223)
            howMany = random.randint(1, 5)
            for iterator in range(0, howMany):
                person = Person.Person(self.values, self.counter)
                print(Colors.WARNING, '[%d]\tToken %d has been generate' % (self.scheduler.currentTime, person.id), Colors.ENDC)
                self.scheduler.afegirEsdeveniment(Event(self.entry, self.scheduler.currentTime, EventType.EnterBuilding, person))
                self.counter += 1
            time = self.scheduler.currentTime + random.randint(10, 60)
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.GeneratePeople, None))

    def deleteToken(self, token):
        print(Colors.WARNING, '[%d]\tToken %d is leaving at home' % (self.scheduler.currentTime, token.id), Colors.ENDC)
        self.home += 1
        del token

    def tractarEsdeveniment(self, event):
        if event.type == EventType.GeneratePeople:
            self.newToken()
        elif event.type == EventType.DeletePerson:
            self.deleteToken(event.entitat)
