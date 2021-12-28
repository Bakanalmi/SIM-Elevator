import matplotlib.pyplot as plt
from event.Event import Event
from event.Constants import *


class Metrics:
    def __init__(self, scheduler, values, title):
        self.timeOut = values.get('time').get('to')
        self.cycle = values.get('time').get('metrics_cycle')
        self.start = values.get('time').get('from')
        self.scheduler = scheduler
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
        now = self.start + self.scheduler.currentTime / 3600
        self.gather_lapses.append(now)

        # ocupació pisos
        for key, floor in self.floors.items():
            if key == 0:
                howMany = len(floor.peopleWaitingPar) + len(floor.peopleWaitingImpar)
                if key not in self.ocupation_floor:
                    self.ocupation_floor[key] = [howMany]
                else:
                    self.ocupation_floor[key].append(howMany)
            else:
                howMany = len(floor.peopleWaiting)
                if key not in self.ocupation_floor:
                    self.ocupation_floor[key] = [howMany]
                else:
                    self.ocupation_floor[key].append(howMany)

        # Temps espera
        if len(self.waiting_lapse_value) > 0:
            wait_avg = sum(self.waiting_lapse_value) / len(self.waiting_lapse_value)
            self.waiting_values.append(wait_avg)
            self.waiting_lapse_value.clear()
        else:
            self.waiting_values.append(0)

        if now < self.timeOut:
            time = self.scheduler.currentTime + self.cycle
            self.scheduler.afegirEsdeveniment(Event(self, time, EventType.UpdateMetrics, None))

    def build(self):
        dashboard = self.figure.add_subplot(1, 1, 1)
        dashboard.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

        arribades = self.figure.add_subplot(3, 1, 1)

        ocupacio_global = self.figure.add_subplot(3, 1, 2)

        esperes = self.figure.add_subplot(3, 1, 3)

        arribades.set_title('Ocupació pl. baixa')
        arribades.bar(self.gather_lapses, self.ocupation_floor[0])

        ocupacio_global.set_title('Ocupació pls. sups.')
        for key, floor in self.ocupation_floor.items():
            if key > 0:
                ocupacio_global.plot(self.gather_lapses, floor)

        esperes.set_title('Temps espera')
        esperes.bar(self.gather_lapses, self.waiting_values)

        plt.suptitle(self.title)

    def show(self):
        self.build()
        plt.show()

    def waiting(self, time):
        self.waiting_lapse_value.append(abs(time))

    def set_resource_elevators(self, elevator):
        self.elevators[elevator.id] = elevator

    def set_resource_floors(self, floors):
        for key, floor in floors.items():
            self.floors[key] = floor
            floor.set_metrics(self)

    def tractarEsdeveniment(self, event):
        if event.type == EventType.UpdateMetrics:
            self.gather()