
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
        self.door = True    # Porta de l'ascensor
        self.idleb = False

    def setUp(self, floors):
        self.floors = floors

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




    def moviment(self):


    def stop_floor(self):

