from objects import elevator, factory, floor as obj_floor
from resources import stairs as res_stairs
from metrics import simplot
import simpy

def setup(values):
    env = simpy.Environment()
    plot = simplot.Metrics(env, values, "Alternating elevators strategy")
    env.process(plot.gather())
    
    creator = None
    floors_parell = {}
    floors_senars = {}
    # Creació dels pisos i classificació entre parells i sernars
    for n_floor in range(0, values.get('environment').get('n_floors')+1):
        floor = obj_floor.Floor(env, values, n_floor)
        floor.metrics = plot

        if n_floor == 0 or n_floor%2 == 0:
            floors_parell[n_floor] = floor
        if n_floor == 0 or n_floor%2 != 0:
            floors_senars[n_floor] = floor

        if n_floor == 0:
            creator = factory.Token(env, floor, values)
            floor.home = creator
            env.process(creator.new_token())

    plot.set_resource_floors(floors_parell)
    plot.set_resource_floors(floors_senars)

    # Creació de l'escala
    stairs = res_stairs.Stairs(env, values)
    stairs.set_floors(floors_parell)
    stairs.set_floors(floors_senars)

    # Creació dels ascensors i assignació dels pisos disponibles
    for n_elev in range(0, values.get('environment').get('n_elevator')):
        elev = elevator.Elevator(env, values, n_elev)
        plot.set_resource_elevators({n_elev: elev})
        if n_elev%2 == 0:
            elev.set_floors(floors_parell)
            for key in floors_parell:
                floors_parell[key].set_elevator(n_elev, elev)
                floors_parell[key].set_stairs(stairs)
        else:
            elev.set_floors(floors_senars)
            for key in floors_senars:
                floors_senars[key].set_elevator(n_elev, elev)
                floors_senars[key].set_stairs(stairs)

    print("\tAlternating strategy: ready")
    return env, plot