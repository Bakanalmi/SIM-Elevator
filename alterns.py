from objects import elevator
import simpy

def setup(env, time, values):
    env = simpy.Environment()

    elev = elevator.Elevator()
    env.process(elev.behaviour(env))

    print("\tAlternating strategy: ready")
    env.run(until=time)