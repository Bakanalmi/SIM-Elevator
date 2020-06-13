import simpy

class Persona:
    def __init__(self):
        self.entry_time = 0     # Hora (en segons) en la qual l'individu entra a treballar
        self.working_time = 0   # Temps total (en segons) de la jornada laboral

        self.lunch_hour = 0 # Hora (en segons) en la qual l'individu va a dinar
        self.lunch_time = 0 # Temps (en segons) que triga l'individu en dinar

        self.office_floor = 12  # Pis on treballa l'individu
        self.walker = False     # Prefereix les escales a l'ascensor

        self.current = 0    # Pis on es troba actualment el individu