import simpy

class Persona:
    entry_time: int     # Hora (en segons) en la qual l'individu entra a treballar
    working_time: int   # Temps total (en segons) de la jornada laboral
    
    lunch_hour: int     # Hora (en segons) en la qual l'individu va a dinar
    lunch_time: int     # Temps (en segons) que triga l'individu en dinar

    office_floor: int   # Pis on treballa l'individu
    walker: bool        # Prefereix les escales a l'ascensor