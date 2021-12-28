import Scheduler
from util import parser
import sys


class Main:
    values_path = './values.yaml'

    def __init__(self):
        self.values = parser.load_simulation_values(self.values_path)
        print("Setting up scheduler environment.")
        self.scheduler = Scheduler.ElevatorSimulation(self.values)

    def run(self):
        print("Running scheduler")
        self.scheduler.run()


if __name__ == "__main__":
    main = Main()
    main.run()
