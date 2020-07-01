# SIM-Elevator-Strategy

Implementació en __Python__ d'un simulador d'esdeveniments discrets (mitjançant la llibreria __Simpy__) per a l'assignatura de simulació (SIM) de la Facultat d'Informàtica de Barcelona (FiB - UPC).

## Descripció del sistema

En aquesta entrega hem decidit enfocar-nos en la proposta d’analitzar l’impacte de dues polítiques d'ús en un sistema de quatre ascensors.

L’escenari que es planteja, doncs, consta de quatre ascensors que pugen i baixen a través d’un sistema de dotze plantas en total. D’aquesta manera, es vol saber com afecten les següents estratègies en la coordinació dels ascensors i en l’exercici de les múltiples tasques (transportar persones):
- `Alternant`: Dos ascensors es desplacen únicamente entre plantes parelles, mentres els altres dos ho fan únicament a plantes senars. Òbviament la planta baixa és comuna en ambdós casos.

- `Express`: Tots els ascensors arriben a totes les plantes, no obstant un dels ascensors és de capacitat reduïda (a la meitat dels demés) però triga menys entre trajectes.

## Suposicions

A partir de la definició anterior, nosaltres hem volgut suposar en quina situació podria donar-se el cas d’un sistema així. La raó d’això és conèixer ben bé l’entorn de la simulació per tal de que la implementació final s’ajusti el màxim possible a un cas real.
Així doncs, el nostre model serà el d’un edifici d’oficines on els treballadors hi van a fer la seva jornada laboral, i després se n'en tornem a casa.

## Memoria

Per entendre en detall com s'ha definit el sistema, així com tots els elements que el conformen i les seves implementacions és recomanable donar un cop d'ull a la [memoria del projecte](./memoria.pdf)

## Equip

- [Hèctor Morales Carnicé](https://github.com/HectorMRC)
- [Joan Pont Martoris](https://github.com/)

##### Qualificació obtinguda: 10
