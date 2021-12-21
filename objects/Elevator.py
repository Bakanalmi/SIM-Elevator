import time

from entities.person import *
from event.Event import Event
from event.Constants import *
import bisect

class Elevator:

    def __init__(self, values, scheduler, ident):


        self.id = ident
        self.scheduler = scheduler

        self.velocity = values.get('elevators').get('velocity')
        self.waiting = values.get('elevators').get('waiting')
        self.capacity = values.get('elevators').get('capacity')
        self.currentFloor = 0    # pis actual al qual es troba l'ascensor
        self.eleUpper = True   # True si, i només si, l'ascensor està pujant
        self.floors = {}    # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.totIn = []      # Individus a l'ascensor
        self.totOut = []     # Invidus
        self.door = False    # Porta de l'ascensor(True = oberta, False = tancada)
        self.idleb = True #Ascensor idle
        self.floorsToGoIn = []
        self.floorsToGoOut = []
        self.state = State.LOCK

    def setUp(self, floors):
        self.floors = floors

    def tractarEsdeveniments(self, event, person):
        if event.type == EventType.TrucarAscensor:
            if person.currentFloor == 0 and person.currentFloor == self.currentFloor and self.capacity > self.tot and self.eleUpper:
                self.personPlantaCeroTrucaYPuja(person)
            elif person.currentFloor > 0 and self.capacity > self.tot and self.eleUpper and self.totIn:
                self.personEsperaAscensorNoPlantaCero(person)
            elif person.currentFloor > 0 and self.capacity > self.tot and self.eleUpper and not self.totIn:
                self.personaEsperantAPlantaSuperiorPuja(person)



    def personPlantaCeroTrucaYPuja (self, person):
        if self.state == State.LOCK: self.state = State.UNLOCK #Obre porta
        personaPujaAscensor = Event(self, time.time(), EventType.GetElevator, person)
        self.scheduler.afegirEsdeveniment(personaPujaAscensor)
        self.totIn.append(person)
        self.totIn.sort(key=lambda x: x.dest)
        self.floorsToGoIn.append(person.dest)

    def personEsperaAscensorNoPlantaCero(self, person):
        personaEsperantAscensor = Event(self, time.time(), EventType.PersonaEspera, person)
        self.scheduler.afegirEsdeveniment(personaEsperantAscensor)
        self.floorsToGoOut.append(person.dest)

    def personaEsperantAPlantaSuperiorPuja(self, person):
        time = self.scheduler.currentTime + self.velocity*(person.currentFloor - self.currentFloor)
        personaPuja = Event(self, time, EventType.GetElevator)
        self.scheduler.afegirEsdeveniment(personaPuja)


    def simulationStart(self):
        self.state=State.ACCESSS
        self.scheduler.afegirEsdeveniment(Event(self,self.tempsCicle,EventType.Access,True))
        self.ciclesTotals=0






    def run(self):
        while True:
            if not self.idle:
                self.transferencia
                self.moving
            else:
                self.idle




    def idle(self):
        print('Ascensor %d idle' % (self.id))
        
    def transferencia(self):


    def


    def moviment(self):


    def stop_floor(self):

