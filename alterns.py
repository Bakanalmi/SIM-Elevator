from objects import elevator
import simpy

def setup(values):
    env = simpy.Environment()
    for n_elev in range(0, values.get('environment').get('n_elevator')):
        elev = elevator.Elevator(env)
        elev.multiple = n_elev%2

    print("\tAlternating strategy: ready")
    return env