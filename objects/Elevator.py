
class Elevator:

    def __init__(self, values, ident):
        self.id = ident

        self.velocity = values.get('elevators').get('velocity')
        self.waiting = values.get('elevators').get('waiting')
        self.capacity = values.get('elevators').get('capacity')
        self.current = 0    # pis actual al qual es troba l'ascensor
        self.upper = True   # True si, i només si, l'ascensor està pujant
        self.floors = {}    # Pisos als quals pot accedir l'ascensor (tupla{num_pis, instancia})
        self.over = []      # Individus a l'ascensor
        self.door = True    # Porta de l'ascensor

    def setUp(self, floors):
        self.floors = floors

    def run(self):


    def idle(self):

        
    def transferencia(self):


    def moviment(self):
