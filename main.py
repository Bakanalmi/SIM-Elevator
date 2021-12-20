from util import parser
import alterns as alt_strategy
import express as xps_strategy
import sys, random

values_path = './values.yaml'
if len(sys.argv) > 1:
    values_path = sys.argv[1]


def main():
    print("Parsing values from", values_path)
    values = parser.load_simulation_values(values_path)
    simulation = values.get('simulation')
    lapse = simulation.get('time')
    strategy = simulation.get('strategy')
    time = 3600 * (lapse.get('to') - lapse.get('from'))
    random.seed(simulation.get('seed'))

    if strategy <= 1:
        print("Setting up alternating environment.")
        alterns, plot = alt_strategy.setup(simulation)
        print("Running alternating strategy")
        alterns.run(until=time)

        plot.show()

    if strategy < 1 or strategy == 2:
        print("Setting up express environment.")
        express, plot = xps_strategy.setup(simulation)
        print("Running express strategy")
        express.run(until=time)

        plot.show()


if __name__ == "__main__":
    main()
