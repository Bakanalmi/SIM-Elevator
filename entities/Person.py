

class Persona:
    def __init__(self, values, ident):
        self.latest = 0
        self.id = ident

        upper = values.get('environment').get('n_floors')
        floor = 0

        choose_stairs = 0
        self.walker = values.get('environment').get('stairs') and choose_stairs > values.get('stairs').get('range')

        self.currentFloor = 0
        self.dest = floor
