from objects import elevator, factory, floor as obj_floor
import simpy

def setup_xpress(env, values):
    xpress_id = values.get('environment').get('n_elevator')-1
    elev = elevator.Elevator(env, values, xpress_id)

    if 'elevators' in values: # overriding values
        if 'express' in values.get('elevators'):
            elev.velocity = values.get('elevators').get('express')
        if 'capacity' in values.get('elevators'):
            elev.capacity = values.get('elevators').get('capacity')/2

def setup(values):
    env = simpy.Environment()
    floors = []

    # Creació dels pisos i classificació entre parells i sernars
    for n_floor in range(0, values.get('environment').get('n_floors')+1):
        floor = obj_floor.Floor(env, n_floor)
        floors.append(floor)

        if n_floor == 0:
            creator = factory.Token(env, floor, values)
            env.process(creator.new_token())

    for n_elev in range(0, values.get('environment').get('n_elevator')-1):
        elev = elevator.Elevator(env, values, n_elev)
        for floor in floors:
            floor.set_elevator(n_elev, elev)

    setup_xpress(env, values)
    print("\tExpress strategy: ready")
    return env