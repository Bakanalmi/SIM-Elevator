from objects import elevator
import simpy

def setup_xpress(env, values):
    xpress_id = values.get('environment').get('n_elevator')-1
    elev = elevator.Elevator(env, xpress_id)

    if 'elevators' in values:
        if 'express' in values.get('elevators'):
            elev.velocity = values.get('elevators').get('express')
        if 'waiting' in values.get('elevators'):
            elev.waiting = values.get('elevators').get('waiting')
        if 'capacity' in values.get('elevators'):
            elev.capacity = values.get('elevators').get('capacity')/2

def setup(values):
    env = simpy.Environment()
    for n_elev in range(0, values.get('environment').get('n_elevator')-1):
        elev = elevator.Elevator(env, n_elev)
        elev.module = -1

        if 'elevators' in values:
            if 'velocity' in values.get('elevators'):
                elev.velocity = values.get('elevators').get('velocity')
            if 'waiting' in values.get('elevators'):
                elev.waiting = values.get('elevators').get('waiting')
            if 'capacity' in values.get('elevators'):
                elev.capacity = values.get('elevators').get('capacity')

    setup_xpress(env, values)
    print("\tExpress strategy: ready")
    return env