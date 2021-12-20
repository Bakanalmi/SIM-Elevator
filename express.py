from objects import elevator, factory, floor as obj_floor
from resources import stairs as res_stairs
from metrics import simplot
import simpy

def setup_xpress(env, values, all_floors):
    xpress_id = values.get('environment').get('n_elevator')-1
    elev = elevator.Elevator(env, values, xpress_id)
    elev.set_floors(all_floors)

    elev.capacity = elev.capacity/2
    elev.velocity = values.get('elevators').get('express')
    
    for key in all_floors:
            all_floors[key].set_elevator(xpress_id, elev)

def setup(values):
    env = simpy.Environment()
    plot = simplot.Metrics(env, values,"Express elevator strategy")
    env.process(plot.gather())
    all_floors = {}

    # Creació dels pisos i classificació entre parells i sernars
    for n_floor in range(0, values.get('environment').get('n_floors')+1):
        floor = obj_floor.Floor(env, values, n_floor)
        floor.metrics = plot
        all_floors[floor.floor] = floor

        if n_floor == 0:
            creator = factory.Token(env, floor, values)
            floor.home = creator
            env.process(creator.new_token())

    plot.set_resource_floors(all_floors)

    stairs = res_stairs.Stairs(env, values)
    stairs.set_floors(all_floors)

    for n_elev in range(0, values.get('environment').get('n_elevator')-1):
        elev = elevator.Elevator(env, values, n_elev)
        plot.set_resource_elevators({n_elev: elev})

        elev.set_floors(all_floors)
        for key in all_floors:
            all_floors[key].set_elevator(n_elev, elev)
            all_floors[key].set_stairs(stairs)

    setup_xpress(env, values, all_floors)
    print("\tExpress strategy: ready")
    return env, plot