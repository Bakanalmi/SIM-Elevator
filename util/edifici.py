

class edifici:
    def __init__(self, values):
        self.ascensors = values.get('environment').get('n_elevator')
        self.plantas = values.get('environment').get('n_floors')
        self.cap_plantas = values.get('environment').get('cap_floor')


