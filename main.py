from util import parser
from objects import elevator
import alterns as alt_strategy
import express as xps_strategy
import simpy, sys

alterns = simpy.Environment()
express = simpy.Environment()

values_path = './values.yaml'
if len(sys.argv) > 1:
        values_path = sys.argv[1]

def main():
    print("Parsing values from", values_path)
    values = parser.load_simulation_values(values_path)
    simulation = values.get('simulation')
    time = simulation.get('time')
    strategy = simulation.get('strategy')
    time = 3600 * (time.get('to')-time.get('from'))
    
    print("Setting up environments...")
    if strategy <= 1:
        alt_strategy.setup(alterns, time, simulation)

    if strategy < 1 or strategy == 2:
        xps_strategy.setup(express, time, simulation)

if __name__ == "__main__":
    main()