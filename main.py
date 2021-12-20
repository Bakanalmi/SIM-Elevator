from event.Event import Event
from util import parser
from event.Constants import *
import sys

class Main:

    values_path = './values.yaml'
    if len(sys.argv) > 1:
        values_path = sys.argv[1]

    def __init__(self):
        self.simulationStart = Event(self, 0, EventType.SimulationStart, None)

    def run(self):
        print("Parsing values from", self.values_path)
        values = parser.load_simulation_values(self.values_path)
        simulation = values.get('simulation')
        lapse = simulation.get('time')
        time = 3600 * (lapse.get('to') - lapse.get('from'))

        print("Setting up alternating environment.")
        alterns, plot = alt_strategy.setup(simulation)
        print("Running alternating strategy")
        alterns.run(until=time)

        plot.show()


if __name__ == "__main__":
    main()
