from enum import Enum


class State(Enum):
    SERVICE = 1
    LOCK = 2
    UNLOCK = 3


class EventType(Enum):
    TrucarAscensor = 1
    GetElevator = 2
    PersonaEspera = 3
    FinishWork = 4
    GetStairs = 5
    StartWorking = 6
    GeneratePeople = 7
    SimulationStart = 8
    EnterBuilding = 9
    DeletePerson = 10


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKRARO = '\033[97m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
