from objects import elevator
from resources import floor as obj_floor
import simpy

def setup(values):
    env = simpy.Environment()
    
    floors_parell = {}
    floors_senars = {}
    # Creació dels pisos i classificació entre parells i sernars
    for n_floor in range(0, values.get('environment').get('n_floors')+1):
        floor = obj_floor.Floor(env, n_floor)
        if n_floor == 0 or n_floor%2 == 0:
            floors_parell[n_floor] = floor
        if n_floor == 0 or n_floor%2 != 0:
            floors_senars[n_floor] = floor

    # Creació dels ascensors i assignació dels pisos disponibles
    for n_elev in range(0, values.get('environment').get('n_elevator')):
        elev = elevator.Elevator(env, n_elev)

        if 'elevators' in values:
            if 'velocity' in values.get('elevators'):
                elev.velocity = values.get('elevators').get('velocity')
            if 'waiting' in values.get('elevators'):
                elev.waiting = values.get('elevators').get('waiting')
            if 'capacity' in values.get('elevators'):
                elev.capacity = values.get('elevators').get('capacity')

        if n_elev%2 == 0:
            elev.set_floors(floors_parell)
            for key in floors_parell:
                floors_parell[key].set_elevator(n_elev, elev)
        else:
            elev.set_floors(floors_senars)
            for key in floors_senars:
                floors_senars[key].set_elevator(n_elev, elev)

    print("\tAlternating strategy: ready")
    return env