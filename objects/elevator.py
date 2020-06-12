import simpy

class Elevator:
    velocity: int   # Temps (en segons) que triga entre pisos consecutius
    multiple: int   # Només para en pisos múltiples de *multiple
    upper: bool     # True si, i només si, l'ascensor està pujant
    parades: []     # Pisos als qual s'espera que pari l'ascensor

    def behaviour(self, env):
        while True:
            print('Start parking at %d' % env.now)
            parking_duration = 5
            yield env.timeout(parking_duration)

            print('Start driving at %d' % env.now)
            trip_duration = 2
            yield env.timeout(trip_duration)