from enum import Enum


class State(Enum):
    IDLE = 1
    MOVEMENT = 2
    TRANSFER = 3


class EventType(Enum):
    CallUp = 1
    CallDown = 2
    GetPeopleInElevator = 3
    GetPeopleOutElevator = 4
    Empty = 5
    SelectFloor = 6
    FinishWorking = 7
    GetStairs = 8
    StartWorking = 9
    GeneratePeople = 10
    SimulationStart = 11
    EnterBuilding = 12
    DeletePerson = 13
    ChangeFloor = 14


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
