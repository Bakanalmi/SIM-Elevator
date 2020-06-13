from util import parser
from objects import elevator
import alterns as alt_strategy
import express as xps_strategy
import simpy, sys

values_path = './values.yaml'
if len(sys.argv) > 1:
        values_path = sys.argv[1]

def main():
    print("Parsing values from", values_path)
    values = parser.load_simulation_values(values_path)
    simulation = values.get('simulation')
    lapse = simulation.get('time')
    strategy = simulation.get('strategy')
    time = 3600 * (lapse.get('to')-lapse.get('from'))
    
    print("Setting up alternating environment.")
    if strategy <= 1:
        alterns = alt_strategy.setup(simulation)
        print("Running alternating strategy")
        alterns.run(until=time)

    # print("Setting up express environment.")
    # if strategy < 1 or strategy == 2:
    #     express = xps_strategy.setup(simulation)
    #     print("Running express strategy")
    #     express.run(until=time)

if __name__ == "__main__":
    main()