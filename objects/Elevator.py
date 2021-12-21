from entities import person
from event.Event import Event
from event.Constants import *
import bisect

class Elevator:

    def __init__(self, values, ident):
        self.id = ident


        self.velocity = values.get('elevators').get('velocity')
        self.waiting = values.get('elevators').get('waiting')
        self.capacity = values.get('elevators').get('capacity')
        self.currentFloor = 0    # pis actual al qual es troba l'ascensor
        self.eleUpper = True   # True si, i només si, l'ascensor està pujant
        self.floors = {}    # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.tot = []      # Individus a l'ascensor
        self.door = False    # Porta de l'ascensor(True = oberta, False = tancada)
        self.idleb = True #Ascensor idle
        self.floorsToGoIn = []
        self.floorsToGoOut = []

    def setUp(self, floors):
        self.floors = floors

    def tractarEsdeveniments(self, event, person):
        if (event.type == EventType.TrucarAscensor):
            if (person.currentFloor == self.currentFloor and self.capacity > self.tot and self.eleUpper):
                self.door = True #Obre porta
                self.personaPujaAscensor = Event(self, 0, EventType.pujarAscensor)
                self.eventList.append()
                self.tot.append(person)
                self.tot.sort(key=lambda x: x.dest)
                self.floorsToGoIn.append(person.dest)
            elif (person.currentFloor > self.currentFloor and self.capacity > self.tot and self.eleUpper):


    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        bisect.insort(self.eventList, event)






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

