import simpy

class Generator:
    def __init__(self):
        self.env = env

        self.required = 150 # Energia requerida a cada segons de funcionament per kilo de pes a moure
        self.consumed = 0   # Energia distribuida pel generador
        self.latest = 0     # Hora en la qual s'ha posat en marxa el generador

    def on(self):
        print('[%d]\tGenerator is On'  % (self.env.now))

    def off(self):
        print('[%d]\tGenerator is Off'  % (self.env.now))
