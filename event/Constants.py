from enum import Enum
class State(Enum):
    SERVICE = 1
    LOCK = 2
    UNLOCK  = 3
    ACCESSE = 4
    ACCESSS = 5
    ACCESSO = 6
    ACCESSN = 7

class EventType(Enum):
    TrucarAscensor=1
    PujarAscensor=2
    Tranfer=3
    Cycle=4
    StepIn=5
    Access=6
    SimulationStart=7

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKRARO= '\033[97m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
