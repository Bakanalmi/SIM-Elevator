import simpy

class Generator:
    def __init__(self, env, values):
        self.env = env
        self.required = values.get('elevators').get('required')
        self.consumed = 0   # Energia distribuida pel generador
        self.latest = 0     # Hora en la qual s'ha posat en marxa el generador

    def on(self):
        print('[%d]\tGenerator is On'  % (self.env.now))
        self.latest = self.env.now

    def off(self, howmany):
        print('[%d]\tGenerator is Off'  % (self.env.now))
        self.consumed += abs(self.env.now - self.latest) * self.required * howmany
