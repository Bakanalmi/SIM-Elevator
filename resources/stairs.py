import time


class Stairs:
    def __init__(self, values):
        self.velocity = values.get('stairs').get('velocity')
        self.floors = {}

    def setUp(self, floors):
        for key, floor in floors.items():
            self.floors[key] = floor

    def request(self, person):
        print('[%d]\tToken %d is taking the stairs.' % (person.id))
        floor = self.floors[person.destination]
        tempsEscales = floor * self.velocity
        time.sleep(tempsEscales)
        floor.entering(person)
