from event.Event import Event
from event.Constants import *
import Scheduler
from util import parser
import sys


class Main:
    values_path = './values.yaml'
    if len(sys.argv) > 1:
        values_path = sys.argv[1]

    def __init__(self):
        self.values = parser.load_simulation_values(self.values_path)
        self.simulation = self.values.get('simulation')
        self.lapse = self.simulation.get('time')
        self.time = 3600 * (self.lapse.get('to') - self.lapse.get('from'))
        print("Setting up scheduler environment.")
        self.scheduler = Scheduler.ElevatorSimulation(self.values)

    def run(self):
        print("Running scheduler")
        self.scheduler.setup(self.simulation)


if __name__ == "__main__":
    main = Main()
    main.run()
