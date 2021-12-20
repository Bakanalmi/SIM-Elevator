import matplotlib.pyplot as plt


class Metrics:
    def __init__(self, env, values, title):
        self.env = env
        self.start = values.get('time').get('from')
        self.timeout = values.get('metrics')
        self.title = title

        self.elevators = {}
        self.floors = {}
        self.gather_lapses = []

        self.ocupation_floor = {}
        self.consumption_elev = {}

        self.waiting_values = []
        self.waiting_lapse_value = []

        self.figure = plt.figure()

    def gather(self):
        while True:
            now = self.env.now/3600 + self.start
            self.gather_lapses.append(now)

            # ocupació pisos
            for key, floor in self.floors.items():
                howmany = len(floor.waiting)
                if key not in self.ocupation_floor:
                    self.ocupation_floor[key] = [howmany]
                else:
                    self.ocupation_floor[key].append(howmany)

            # Temps espera
            if len(self.waiting_lapse_value) > 0:
                wait_avg = sum(self.waiting_lapse_value) / len(self.waiting_lapse_value) 
                self.waiting_values.append(wait_avg)
                self.waiting_lapse_value.clear()
            else:
                self.waiting_values.append(0)

            yield self.env.timeout(self.timeout)

    def build(self):
        dashboard = self.figure.add_subplot(1, 1, 1)
        dashboard.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

        arribades = self.figure.add_subplot(3, 2, 1)

        ocupacio_global = self.figure.add_subplot(3, 2, 2)
        
        esperes = self.figure.add_subplot(3, 1, 2)
        consum = self.figure.add_subplot(3, 1, 3) # divisió cap  munt, divisió esquerra, casella horitzontal

        arribades.set_title('Ocupació pl. baixa')
        arribades.bar(self.gather_lapses, self.ocupation_floor[0])

        ocupacio_global.set_title('Ocupació pls. sups.')
        for key, floor in self.ocupation_floor.items():
            if key > 0:
                ocupacio_global.plot(self.gather_lapses, floor)

        esperes.set_title('Temps espera')
        esperes.bar(self.gather_lapses, self.waiting_values)

        consum.set_title('Consum energetic')
        for key, cons_elev in self.consumption_elev.items():
            consum.plot(self.gather_lapses, cons_elev)
    
        plt.suptitle(self.title)

    def show(self):
        self.build()
        plt.show()

    def waiting(self, time):
        self.waiting_lapse_value.append(abs(time))

    def set_resource_elevators(self, elevators):
        for key, elev in elevators.items():
            self.elevators[key] = elev

    def set_resource_floors(self, floors):
        for key, floor in floors.items():
            self.floors[key] = floor